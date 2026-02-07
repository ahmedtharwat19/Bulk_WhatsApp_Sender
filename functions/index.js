const functions = require("firebase-functions");
const admin = require("firebase-admin");

admin.initializeApp();

exports.verifyLicense = functions.https.onRequest(async (req, res) => {
  try {
    const { hwid, licenseKey, app } = req.body || {};

    if (!hwid || !licenseKey || !app) {
      return res.status(400).json({ valid: false, error: "MISSING_FIELDS" });
    }

    const docRef = admin.firestore().collection("licenses").doc(licenseKey);
    const doc = await docRef.get();

    if (!doc.exists) {
      return res.json({ valid: false, error: "LICENSE_NOT_FOUND" });
    }

    const data = doc.data();

    if (!data.active || data.app !== app) {
      return res.json({ valid: false, error: "LICENSE_INACTIVE" });
    }

    // Bind HWID
    if (!data.hwid) {
      await docRef.update({ hwid });
    } else if (data.hwid !== hwid) {
      return res.json({ valid: false, error: "HWID_MISMATCH" });
    }

    const now = new Date();
    const end = new Date(data.end_date);

    if (!data.end_date || isNaN(end.getTime())) {
      return res.json({ valid: false, error: "INVALID_END_DATE" });
    }

    if (now > end) {
      return res.json({ valid: false, expired: true });
    }

    await docRef.update({ last_check: now.toISOString() });

    return res.json({
      valid: true,
      plan: data.plan,
      end_date: data.end_date,
    });

  } catch (err) {
    console.error("VERIFY_LICENSE_ERROR:", err);
    return res.status(500).json({ valid: false, error: "SERVER_ERROR" });
  }
});
