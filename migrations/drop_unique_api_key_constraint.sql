-- Migration: Drop unique_api_key_per_position constraint
-- Date: 2026-02-20
-- Reason: Allow positions to be saved without API keys assigned
--         API key uniqueness is now enforced in application code when assigning

-- Drop the constraint that prevents NULL API keys
ALTER TABLE position_configs 
DROP CONSTRAINT IF EXISTS unique_api_key_per_position;

-- Verify constraint is gone
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'position_configs' 
AND constraint_type = 'UNIQUE';

-- Expected result: Should NOT see unique_api_key_per_position in results
-- Should only see:
--   - position_configs_user_id_position_name_key (UNIQUE on user_id, position_name)
--   - position_configs_user_id_protocol_nft_id_network_key (UNIQUE on user_id, protocol, nft_id, network)
