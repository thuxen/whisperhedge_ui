# Frequently Asked Questions

## Getting Started

**Q: Do I need to create a password?**
A: No! WhisperHedge uses passwordless magic link authentication. Just enter your email and click the link we send you.

**Q: How do I add my first position?**
A: See our [step-by-step guide](getting-started/first-position.md).

**Q: What protocols do you support?**
A: Currently Hyperliquid and Uniswap V3. [See all supported protocols →](position-setup/supported-protocols.md)

## API Keys & Security

**Q: Why do you need my API keys?**
A: To read your position data and calculate metrics. We only require read-only access.

**Q: Can you trade with my API keys?**
A: No. We only accept read-only keys that cannot execute trades or move funds.

**Q: Why one API key per position?**
A: For security isolation. If one key is compromised, only that position is affected. [Learn more →](api-keys/one-key-per-position.md)

**Q: How often should I rotate API keys?**
A: Every 3-6 months is recommended. [Rotation guide →](api-keys/rotating-keys.md)

## Pricing & Plans

**Q: Is there a free tier?**
A: Yes! Free tier supports up to $10K TVL and 3 positions. [See all plans →](features/plan-tiers.md)

**Q: Can I upgrade/downgrade anytime?**
A: Yes. Upgrades are instant, downgrades take effect next billing cycle.

**Q: What happens if I exceed my plan limits?**
A: Position updates pause until you upgrade or remove positions. No data is lost.

## Position Tracking

**Q: How often do positions update?**
A: Depends on your plan: Free (15 min), Pro (5 min), Premium (1 min). [Details →](position-setup/tracking-frequency.md)

**Q: Can I manually refresh?**
A: Yes, anytime! Click the refresh button on any position.

**Q: Why isn't my position updating?**
A: Check API key permissions and plan limits. [Troubleshooting guide →](troubleshooting/position-not-updating.md)

## Impermanent Loss

**Q: What is impermanent loss?**
A: The difference between holding tokens vs providing liquidity. [Full explanation →](features/impermanent-loss.md)

**Q: How do you calculate IL?**
A: We compare your current LP value to what you'd have if you just held the tokens.

**Q: Can IL be positive?**
A: Rarely, but yes - in some stable pair scenarios.

## Notifications

**Q: What notifications do you send?**
A: Critical health warnings, significant IL changes, and major value drops. [Details →](features/notifications.md)

**Q: Can I customize notification thresholds?**
A: Coming soon! Currently we use smart defaults.

**Q: Why am I not receiving emails?**
A: Check spam folder and verify notifications are enabled in settings.

## Technical

**Q: Which networks do you support?**
A: Ethereum, Polygon, Arbitrum, Optimism, Base for Uniswap V3. Arbitrum for Hyperliquid.

**Q: Do you have an API?**
A: Coming soon for Premium tier users.

**Q: Is my data secure?**
A: Yes. API keys are encrypted, all data transmitted over HTTPS. [Security details →](security/index.md)

## Account Management

**Q: How do I delete my account?**
A: Go to Settings → Danger Zone → Delete Account. All data is permanently removed.

**Q: Can I export my data?**
A: Contact support to request a data export.

**Q: How do I change my email?**
A: Email change is coming soon. Contact support for now.

## Troubleshooting

**Q: "Invalid API Key" error?**
A: Verify key format, permissions, and subaccount. [Full guide →](troubleshooting/api-key-issues.md)

**Q: Position shows wrong value?**
A: Wait 5-10 minutes for sync, then try manual refresh.

**Q: How do I contact support?**
A: Email support@whisperhedge.com. [Contact details →](troubleshooting/contact-support.md)

## Still Have Questions?

[Contact Support →](troubleshooting/contact-support.md)
