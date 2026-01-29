-- =====================================================
-- MIGRATION: Add protocol field to lp_positions and position_configs
-- Run these commands in Supabase SQL Editor
-- =====================================================

-- Step 1: Add protocol column to lp_positions table (nullable first, then set values, then make NOT NULL)
ALTER TABLE lp_positions 
ADD COLUMN protocol TEXT;

-- Step 2: Set existing positions to uniswap_v3 (since all current positions are Uniswap V3)
UPDATE lp_positions 
SET protocol = 'uniswap_v3' 
WHERE protocol IS NULL;

-- Step 3: Make protocol NOT NULL after setting values
ALTER TABLE lp_positions 
ALTER COLUMN protocol SET NOT NULL;

-- Step 4: Drop old unique constraint on lp_positions
ALTER TABLE lp_positions 
DROP CONSTRAINT IF EXISTS lp_positions_user_id_network_nft_id_key;

-- Step 5: Add new unique constraint including protocol on lp_positions
ALTER TABLE lp_positions 
ADD CONSTRAINT lp_positions_user_id_protocol_network_nft_id_key 
UNIQUE(user_id, protocol, network, nft_id);

-- Step 6: Add protocol column to position_configs table (nullable first, then set values, then make NOT NULL)
ALTER TABLE position_configs 
ADD COLUMN protocol TEXT;

-- Step 7: Set existing configs to uniswap_v3 (since all current positions are Uniswap V3)
UPDATE position_configs 
SET protocol = 'uniswap_v3' 
WHERE protocol IS NULL;

-- Step 8: Make protocol NOT NULL after setting values
ALTER TABLE position_configs 
ALTER COLUMN protocol SET NOT NULL;

-- Step 9: Drop old unique constraint on position_configs (nft_id, network)
ALTER TABLE position_configs 
DROP CONSTRAINT IF EXISTS position_configs_user_id_nft_id_network_key;

-- Step 10: Add new unique constraint including protocol on position_configs
ALTER TABLE position_configs 
ADD CONSTRAINT position_configs_user_id_protocol_nft_id_network_key 
UNIQUE(user_id, protocol, nft_id, network);

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Verify lp_positions has protocol field
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'lp_positions' AND column_name = 'protocol';

-- Verify position_configs has protocol field
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'position_configs' AND column_name = 'protocol';

-- Check all existing positions have protocol set
SELECT COUNT(*) as total_lp_positions, 
       COUNT(CASE WHEN protocol = 'uniswap_v3' THEN 1 END) as uniswap_v3_count
FROM lp_positions;

SELECT COUNT(*) as total_position_configs, 
       COUNT(CASE WHEN protocol = 'uniswap_v3' THEN 1 END) as uniswap_v3_count
FROM position_configs;
