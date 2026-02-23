# Magic Link Authentication

WhisperHedge uses magic link authentication - a passwordless login system that's both more secure and more convenient than traditional passwords.

## How It Works

### The Magic Link Flow

1. **You request a link** - Enter your email on the login or signup page
2. **We send you an email** - Contains a unique, one-time-use link
3. **You click the link** - Opens in your browser and logs you in automatically
4. **You're in!** - Redirected to your dashboard, fully authenticated

### Technical Details

Magic links use the **PKCE (Proof Key for Code Exchange)** flow, which is:

- ✅ More secure than passwords
- ✅ Resistant to phishing attacks
- ✅ No password database to breach
- ✅ Industry-standard authentication

## Benefits of Passwordless Auth

### Security Advantages

**No Password Reuse**
You can't reuse the same password across sites (because there are no passwords!)

**No Password Breaches**
We don't store passwords, so there's nothing to steal in a database breach.

**Phishing Resistant**
Even if someone tricks you into clicking a fake link, they can't use it without access to your email.

**Time-Limited**
Links expire after 1 hour, limiting the window for potential attacks.

### Convenience Benefits

**Nothing to Remember**
No passwords to memorize or write down.

**No Password Resets**
Never deal with "forgot password" flows again.

**Quick Login**
Just check your email and click - faster than typing a password.

**Works Everywhere**
Access your account from any device with email access.

## Using Magic Links

### For Login

1. Go to [whisperhedge.com/login](https://whisperhedge.com/login)
2. Enter your email
3. Click "Send Magic Link"
4. Check your email and click the link

### For Signup

Same process! The system automatically creates your account if it doesn't exist.

!!! info "Automatic Account Creation"
    If you request a magic link for an email that doesn't have an account yet, we'll automatically create one for you when you click the link.

## Link Anatomy

A typical magic link looks like this:

```
https://whisperhedge.com/auth/callback?token_hash=abc123...&type=magiclink
```

**Components:**

- `token_hash` - Unique, one-time authentication token
- `type` - Specifies this is a magic link (vs other auth types)

!!! warning "Never Share Links"
    Magic links are like temporary passwords. Never share them with anyone!

## Troubleshooting

### Link Not Working

**"This magic link has expired"**

Links expire after 1 hour. Request a new one from the login page.

**"Invalid magic link"**

This usually means:

- The link was already used
- The link is malformed (copy/paste error)
- The link is for a different environment

**Redirecting to wrong domain?**

If you're a developer testing locally, you may need to manually edit the link:

```
# Change this:
https://whisperhedge.com/auth/callback?token_hash=abc123...

# To this:
http://localhost:3000/auth/callback?token_hash=abc123...
```

### Email Not Arriving

1. **Check spam folder** - Sometimes magic link emails get filtered
2. **Wait a few minutes** - Email delivery can be delayed
3. **Check email address** - Make sure you typed it correctly
4. **Request a new link** - The old one might have failed to send

### Security Concerns

**"What if someone accesses my email?"**

If someone has access to your email account, they can access any service you use (password reset emails, etc.). Secure your email with:

- Strong email password
- Two-factor authentication on your email
- Regular security checkups

**"Can I use 2FA?"**

Two-factor authentication is coming soon! For now, securing your email account provides similar protection.

## Best Practices

### Keep Your Email Secure

- ✅ Use a strong, unique password for your email
- ✅ Enable 2FA on your email account
- ✅ Don't share email access
- ✅ Log out of email on shared devices

### Link Hygiene

- ✅ Click links promptly (don't let them sit in your inbox)
- ✅ Delete old magic link emails after using them
- ✅ Never share magic links with anyone
- ✅ Request a new link if you're unsure about an old one

## Future Enhancements

We're working on additional authentication options:

- **Two-Factor Authentication (2FA)** - TOTP authenticator app support
- **Biometric Login** - Fingerprint/Face ID on mobile
- **Hardware Keys** - YubiKey and similar devices

See our [coming soon](../coming-soon/advanced-features.md) page for more details.

---

**Next:** [Dashboard Overview →](dashboard-overview.md)
