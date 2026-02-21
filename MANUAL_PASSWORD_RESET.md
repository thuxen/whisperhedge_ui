# Manual Password Reset Process

The automated password reset flow has been disabled due to technical issues with Reflex page rendering.

## When a User Forgets Their Password

### Option 1: Send Magic Link (Recommended)

1. Open **Supabase Dashboard** → **Authentication** → **Users**
2. Find the user by email
3. Click the **"..."** menu next to their name
4. Select **"Send magic link"**
5. User clicks link in email → automatically logged in
6. User can then change password in Settings page (once implemented)

### Option 2: Manually Reset Password

1. Open **Supabase Dashboard** → **Authentication** → **Users**
2. Find the user by email
3. Click **"..."** → **"Reset password"**
4. Enter a temporary password (e.g., `TempPass123!`)
5. Email the user the temporary password
6. Tell them to:
   - Log in with temporary password
   - Go to Settings
   - Change to a permanent password

### Option 3: SQL Editor (Advanced)

```sql
-- Update password directly
UPDATE auth.users 
SET encrypted_password = crypt('temporary_password_123', gen_salt('bf'))
WHERE email = 'user@example.com';
```

## Why Password Reset is Disabled

The `/reset-password` page fails to load despite:
- Identical structure to working pages (login, signup)
- No JavaScript/script components
- Clean Reflex compilation
- No console errors (except unrelated browser extension error)

This appears to be a Reflex framework bug or caching issue that persists even after:
- Deleting `.web` folder
- Restarting service
- Multiple code refactors
- Removing all custom logic

## Future Solution

Implement "Change Password" in Settings page where user is already authenticated, avoiding the need for token extraction from email links.
