#!/usr/bin/env python3
"""
Test script for Chatterbox TTS Gradio API
"""

from gradio_client import Client
import sys

def test_api(server_url):
    """
    Test the Gradio API endpoints
    
    Args:
        server_url: URL of your deployed instance (e.g., "http://your-domain.com" or "http://ip:7860")
    """
    
    print(f"Connecting to {server_url}...")
    
    try:
        client = Client(server_url)
        print("✓ Successfully connected to the server")
        
        # View available API endpoints
        print("\nAvailable API endpoints:")
        print(client.view_api())
        
        # Example 1: Test Text-to-Speech (adjust endpoint name based on actual API)
        print("\n" + "="*60)
        print("Testing Text-to-Speech...")
        print("="*60)
        
        try:
            result = client.predict(
                "Hello, this is a test of the TTS system.",  # text
                "Morgan Freeman_male",  # voice_select
                1.0,  # exaggeration
                0.7,  # temp
                42,   # seed_num
                1.0,  # cfg_weight
                0.1,  # min_p
                0.9,  # top_p
                1.0,  # repetition_penalty
                api_name="/predict"  # Adjust based on actual endpoint
            )
            print(f"✓ TTS generation successful!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"✗ TTS test failed: {e}")
            print("Note: You may need to adjust the API endpoint name and parameters")
        
        # Example 2: Test Multilingual TTS
        print("\n" + "="*60)
        print("Testing Multilingual TTS...")
        print("="*60)
        
        try:
            result = client.predict(
                "Bonjour, comment allez-vous?",  # text
                "Default (French)",  # voice_select
                "fr",  # language_select
                1.0,  # exaggeration
                0.7,  # temp
                42,   # seed_num
                1.0,  # cfg_weight
                api_name="/multilingual"  # Adjust based on actual endpoint
            )
            print(f"✓ Multilingual TTS generation successful!")
            print(f"Result: {result}")
        except Exception as e:
            print(f"✗ Multilingual test failed: {e}")
            print("Note: This endpoint may have a different name")
        
        print("\n" + "="*60)
        print("API Testing Complete!")
        print("="*60)
        print("\nFor detailed API documentation, visit:")
        print(f"{server_url}/api/docs")
        
    except Exception as e:
        print(f"✗ Failed to connect to server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the service is running: sudo systemctl status chatterbox-tts")
        print("2. Check if the port is accessible: curl http://localhost:7860")
        print("3. Verify firewall settings: sudo firewall-cmd --list-all")
        return False
    
    return True


if __name__ == "__main__":
    # Default to localhost if no argument provided
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7860"
    
    print("="*60)
    print("Chatterbox TTS - API Test Script")
    print("="*60)
    print(f"Server: {server_url}\n")
    
    success = test_api(server_url)
    
    if success:
        print("\n✓ All tests completed. Check the results above.")
    else:
        print("\n✗ Tests failed. Check the error messages above.")
        sys.exit(1)
