import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

type ResponseData = {
  message: string;
  error?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  const { from, subject, message } = req.body;

  if (!from || !subject || !message) {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  const API_KEY = process.env.MAILGUN_API_KEY;
  const FROM_EMAIL = process.env.FROM_EMAIL || "feedback@pohwp.dev";
  const TO_EMAIL = process.env.ADMIN_EMAIL;

  if (!API_KEY || !TO_EMAIL) {
    console.error('Missing environment variables: MAILGUN_API_KEY or ADMIN_EMAIL');
    return res.status(500).json({ message: 'Server configuration error' });
  }

  try {
    await axios({
      method: "post",
      url: `https://api.mailgun.net/v3/pohwp.dev/messages`,
      auth: {
        username: "api",
        password: API_KEY,
      },
      params: {
        from: FROM_EMAIL,
        to: TO_EMAIL,
        subject: "New Message From A Visitor: " + subject,
        text: "From: " + from + "\nMessage: " + message,
      },
    });

    return res.status(200).json({ message: 'Email sent successfully' });
  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ 
      message: 'Failed to send email',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
