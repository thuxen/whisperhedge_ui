"""
FastAPI endpoint for Stripe webhooks
This file should be imported and registered with your Reflex app
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..services.stripe_service import verify_webhook_signature
from .stripe_webhook import process_stripe_webhook

# Create router for webhook endpoints
webhook_router = APIRouter(prefix="/api", tags=["webhooks"])


@webhook_router.post("/stripe-webhook")
async def stripe_webhook_endpoint(request: Request):
    """
    Stripe webhook endpoint
    Receives and processes Stripe events
    
    This endpoint:
    1. Verifies the webhook signature
    2. Processes the event (updates database)
    3. Returns 200 OK to Stripe
    """
    try:
        # Get raw body and signature
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        if not sig_header:
            raise HTTPException(status_code=400, detail="Missing stripe-signature header")
        
        # Verify webhook signature
        event = verify_webhook_signature(payload, sig_header)
        
        if not event:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Process the event
        success = process_stripe_webhook(event)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={"status": "success", "event_type": event.get("type")}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Failed to process webhook"}
            )
            
    except Exception as e:
        print(f"Webhook error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@webhook_router.get("/webhook-health")
async def webhook_health():
    """Health check endpoint for webhook service"""
    return {"status": "healthy", "service": "stripe-webhooks"}
