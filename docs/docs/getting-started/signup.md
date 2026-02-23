# Creating Your Account

WhisperHedge uses passwordless authentication for maximum security and convenience. No passwords to remember, no password resets - just simple, secure magic links.

## Sign Up Process

### Step 1: Visit the Sign Up Page

Go to [whisperhedge.com/signup](https://whisperhedge.com/signup)

### Step 2: Enter Your Email

1. Enter your email address in the form
2. Click **"Send Magic Link"**
3. Check your inbox (and spam folder if needed)

!!! info "Email Delivery"
    Magic links are usually delivered within seconds, but can take up to 1-2 minutes during high traffic.

### Step 3: Click the Magic Link

1. Open the email from WhisperHedge
2. Click the **"Confirm Your Account"** button
3. You'll be automatically logged in and redirected to your dashboard

!!! tip "Plain Text Link"
    Can't click the button? Copy and paste the plain text link below the button into your browser.

### Step 4: Complete!

That's it! Your account is now active and you can start adding positions.

## Magic Link Details

### Security Features

- **One-time use** - Each link can only be used once
- **Time-limited** - Links expire after 1 hour
- **Secure tokens** - Uses industry-standard PKCE flow
- **No password storage** - We never store passwords

### Troubleshooting Sign Up

**Email not arriving?**

1. Check your spam/junk folder
2. Make sure you entered the correct email address
3. Wait 2-3 minutes (sometimes there's a delay)
4. Try requesting a new link

**Link expired?**

Magic links expire after 1 hour. Simply request a new one from the [login page](https://whisperhedge.com/login).

**Link not working?**

If you're testing locally, you may need to manually change the URL from `https://whisperhedge.com` to `http://localhost:3000`. See our [magic links guide](magic-links.md) for details.

## Account Information

### What We Collect

During signup, we only collect:

- Your email address
- Account creation timestamp
- Authentication tokens (temporary)

We do **not** collect:

- Passwords
- Personal information
- Payment details (until you upgrade)

See our [data privacy policy](../security/data-privacy.md) for more details.

### Two-Factor Authentication

Coming soon: 2FA via OTP generator app for additional account security.

### Email Verification

Your email is automatically verified when you click the magic link. No additional verification steps needed!

## Next Steps

After signing up:

1. **[Understand Magic Links](magic-links.md)** - Learn how our authentication works
2. **[Explore the Dashboard](dashboard-overview.md)** - Get familiar with the interface
3. **[Set Up API Keys](../api-keys/hyperliquid-keys.md)** - Connect your trading platforms
4. **[Add Your First Position](first-position.md)** - Start tracking

---

**Next:** [Magic Links Explained →](magic-links.md)
