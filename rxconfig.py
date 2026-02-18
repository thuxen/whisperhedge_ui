import reflex as rx

config = rx.Config(
    app_name="web_ui",
    title="WhisperHedge - Automated Liquidity Pool Hedging",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)