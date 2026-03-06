import os
import shutil

# Files to DELETE
files_to_delete = [
    "network_steganography_covert.py",
    "network_stego_core.py",
    "network_stego_examples.py",
    "realtime_network_stego.py",
    "ultrafast_network_stego.py",
    "simple_network_demo.py",
    "simple_realtime_stego.py",
    "fixed_http_header_stego.py",
    "http_network_stego.py",
    "network_steganalysis.py",
    "cloud_covert_channel.py",
    "cloud_exfiltration_demo.py",
    "ai_resistant_demo.py",
    "ai_resistance_visualization.png",
    "blockchain_steganography.py",
    "blockchain_integration_demo.py",
    "ethereum_blockchain_steganography.py",
    "blockchain_receiver.py",
    "blockchain_user_verification.py",
    "secure_blockchain_steganography.py",
    "test_blockchain_config.py",
    "test_blockchain_config_ascii.py",
    "test_contracts_simple.py",
    "test_deployed_contracts.py",
    "deploy_user_registry.py",
    "setup_blockchain.py",
    "multi_layer_stego.py",
    "adaptive_stego.py",
    "simple_app.py",
    "minimal_websocket_chat.py",
    "test_websocket.py",
    "ABSTRACT.md",
    "ANALYSIS_REPORT.md",
    "BLOCKCHAIN_STEGANOGRAPHY_ANALYSIS.md",
    "COMPLETE_PROJECT_README.md",
    "COVERT_CHANNELS_EXPLAINED.md",
    "DELIVERY_SUMMARY.md",
    "DELIVERY.md",
    "ETHEREUM_SETUP_GUIDE.md",
    "GUIDE_EXPLANATION.md",
    "INDEX.md",
    "NETWORK_STEGANOGRAPHY_COMPLETE.md",
    "PRESENTATION_GUIDE.md",
    "PROJECT_ANALYSIS.md",
    "PROJECT_COMPLETE_SUMMARY.md",
    "PROJECT_OVERVIEW.md",
    "README_network.md",
    "RESEARCH_IDEAS.md",
    "WEB_INTERFACE_COMPLETE.md",
    "WEB_INTERFACE_GUIDE.md",
    "WEB_INTERFACE_INDEX.md",
    "requirements_network.txt",
    "requirements_realtime.txt",
    "requirements_unique.txt",
    "requirements_web.txt",
    "verify.py",
    "QUICKSTART.py",
    "test_setup_nav.html",
    "SteganographyVerification.sol",
    "run_web_app.sh",
    "RUN_WEB_APP.bat",
    "cleanup_project.py"
]

# Folders to DELETE
folders_to_delete = [
    "Steganography-for-IP-networks-master",
    "static"
]

print("CLEANING PROJECT...")
removed = 0

for f in files_to_delete:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed: {f}")
        removed += 1

for folder in folders_to_delete:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Removed folder: {folder}")
        removed += 1

print(f"\nDone! Removed {removed} items")
print("\nKEPT FILES:")
print("- advanced_blockchain_steganography.py")
print("- AdvancedSteganographyController.sol")
print("- SecureUserRegistry.sol")
print("- blockchain_config.json")
print("- app.py")
print("- blockchain_web_app.py")
print("- steganography.py")
print("- cli.py")
print("- templates/")
print("- uploads/")
print("- outputs/")
print("- README.md")
print("- BLOCKCHAIN_EXPLANATION.md")
print("- requirements.txt")