# Available Metrics from hedge_state Table

Complete list of metrics available in the QuestDB `hedge_state` table that can be displayed in the UI.

## Currently Implemented ✅

- **lp_value_usd** - Current LP position value in USD
- **hl_account_value** - Hedge account balance in USD
- **total_value** - Combined LP + Hedge value
- **lp_pnl_usd** - LP position profit/loss in USD
- **lp_pnl_pct** - LP position profit/loss percentage
- **time** - Timestamp of last update

## Performance Metrics

### Profit & Loss
- **lp_pnl_usd** - LP position PnL in USD ✅ (implemented)
- **lp_pnl_pct** - LP position PnL percentage ✅ (implemented)
- **lp_il_usd** - Impermanent loss in USD
- **lp_il_pct** - Impermanent loss percentage

### Position Entry
- **lp_entry_price** - Entry price when position was created

## Position Health Metrics

### Range Utilization
- **lp_utilization_pct** - How much of the price range is being utilized (0-100%)
- **lp_distance_to_lower_pct** - Distance to lower price bound as percentage
- **lp_distance_to_upper_pct** - Distance to upper price bound as percentage

### Position State
- **lp_current_ratio** - Current price ratio
- **lp_current_tick** - Current tick in the pool
- **lp_liquidity** - Liquidity amount
- **lp_pa** - Lower price bound
- **lp_pb** - Upper price bound

### Token Amounts
- **lp_token0_amount** - Amount of token0 in position
- **lp_token1_amount** - Amount of token1 in position

### Delta Metrics
- **lp_delta_token0** - Delta exposure for token0
- **lp_ratio_change_pct** - How much ratio has changed since last rebalance
- **lp_last_rebalance_ratio** - Ratio at last rebalance

## Price Metrics

### Hyperliquid Prices
- **hl_price_token0** - Hyperliquid price for token0
- **hl_price_token1** - Hyperliquid price for token1
- **hl_oracle_price_token0** - Oracle price for token0
- **hl_oracle_price_token1** - Oracle price for token1
- **hl_ratio_token1_per_token0** - Price ratio on Hyperliquid

### LP vs HL Basis
- **ratio_lp_vs_hl_basis_bps** - Basis between LP and HL in basis points
- **ratio_lp_vs_hl_basis_pct** - Basis between LP and HL as percentage

## Hedge Position Metrics

### Token 0 Hedge
- **hl_hedge_token0_current** - Current hedge size for token0
- **hl_hedge_token0_target** - Target hedge size for token0
- **hl_hedge_token0_adjustment** - Adjustment needed for token0
- **hl_hedge_token0_notional_usd** - Notional value in USD

### Token 1 Hedge
- **hl_hedge_token1_current** - Current hedge size for token1
- **hl_hedge_token1_target** - Target hedge size for token1
- **hl_hedge_token1_adjustment** - Adjustment needed for token1
- **hl_hedge_token1_notional_usd** - Notional value in USD

### Hedge Metadata
- **hl_hedge_gamma** - Gamma of the hedge
- **hl_hedge_policy** - Hedge policy being used
- **hl_hedge_action_status** - Status of last hedge action

## Account Metrics

### Hyperliquid Account
- **hl_account_value** - Total account value ✅ (implemented)
- **hl_margin_used** - Margin currently used
- **hl_available** - Available margin
- **hl_notional_pos** - Notional position size

## Market Data Metrics

### Token 0 Market Data
- **hl_open_interest_token0** - Open interest for token0
- **hl_day_ntl_vlm_token0** - Daily notional volume for token0
- **hl_funding_rate_token0** - Funding rate for token0
- **hl_premium_token0** - Premium for token0

### Token 1 Market Data
- **hl_open_interest_token1** - Open interest for token1
- **hl_day_ntl_vlm_token1** - Daily notional volume for token1
- **hl_funding_rate_token1** - Funding rate for token1
- **hl_premium_token1** - Premium for token1

## Pool State Metrics

- **lp_pool_tick** - Current tick of the pool
- **lp_pool_sqrt_price_x96** - Square root price (Q96 format)
- **lp_pool_liquidity** - Total pool liquidity
- **lp_pool_is_inverted** - Whether the pool is inverted

## Recommended Metrics to Add Next

### High Priority (User-Facing Performance)
1. **Impermanent Loss** (`lp_il_usd`, `lp_il_pct`) - Shows IL impact
2. **Range Utilization** (`lp_utilization_pct`) - Shows how efficiently range is used
3. **Distance to Bounds** (`lp_distance_to_lower_pct`, `lp_distance_to_upper_pct`) - Shows risk of going out of range

### Medium Priority (Position Health)
4. **Entry Price** (`lp_entry_price`) - Shows where position started
5. **Current vs Entry Ratio** - Calculate from `lp_current_ratio` and `lp_entry_price`
6. **Hedge Efficiency** - Compare `hl_hedge_token0_current` vs `hl_hedge_token0_target`

### Low Priority (Advanced)
7. **Funding Rates** (`hl_funding_rate_token0`, `hl_funding_rate_token1`) - Shows funding costs
8. **Margin Usage** (`hl_margin_used` / `hl_account_value`) - Shows account leverage
9. **Basis Spread** (`ratio_lp_vs_hl_basis_pct`) - Shows arbitrage opportunity

## Display Recommendations

### Main Card (Always Visible)
- Total Value ✅
- LP PnL (USD + %) ✅
- Last Check ✅

### Expandable "Performance" Section
- Impermanent Loss (USD + %)
- Entry Price
- Current Price
- Price Change %

### Expandable "Position Health" Section
- Range Utilization %
- Distance to Lower Bound
- Distance to Upper Bound
- In Range indicator

### Expandable "Hedge Status" Section
- Hedge Efficiency (current vs target)
- Margin Used %
- Funding Rate (if significant)

### Hedging Settings (Currently Collapsible) ✅
- All configuration parameters
