const functions = require("firebase-functions");
const admin = require("firebase-admin");
admin.initializeApp();

exports.verifyLicense = functions.https.onRequest(async (req, res) => {
  const { hwid, license_key, app } = req.body;

  if (!hwid || !license_key) {
    return res.status(400).json({ valid: false });
  }

  const doc = await admin
    .firestore()
    .collection("licenses")
    .doc(license_key)
    .get();

  if (!doc.exists) {
    return res.json({ valid: false });
  }

  const data = doc.data();

  if (!data.active || data.app !== app) {
    return res.json({ valid: false });
  }

  // Bind HWID
  if (!data.hwid) {
    await doc.ref.update({ hwid });
  } else if (data.hwid !== hwid) {
    return res.json({ valid: false, reason: "HWID_MISMATCH" });
  }

  const now = new Date();
  const end = new Date(data.end_date);

  if (now > end) {
    return res.json({ valid: false, expired: true });
  }

  await doc.ref.update({ last_check: now.toISOString() });

  return res.json({
    valid: true,
    plan: data.plan,
    end_date: data.end_date
  });
});
