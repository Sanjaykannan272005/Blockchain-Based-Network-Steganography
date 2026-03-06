#!/usr/bin/env python3
import argparse
import sys
import os
from steganography import SecureSteganography
from enhanced_steganography import EnhancedSteganography
from minimal_video_steganography import MinimalVideoSteganography

def main():
    parser = argparse.ArgumentParser(description='Secure Steganographic Communication CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Enhanced hide command
    hide_parser = subparsers.add_parser('hide', help='Hide data in image/video')
    hide_parser.add_argument('input', help='Input image/video path')
    hide_parser.add_argument('output', help='Output stego image/video path')
    hide_parser.add_argument('-d', '--data', help='Secret data to hide')
    hide_parser.add_argument('-f', '--file', help='File containing secret data')
    hide_parser.add_argument('-p', '--password', required=True, help='Encryption password')
    hide_parser.add_argument('--enhanced', action='store_true', help='Use enhanced security features')
    hide_parser.add_argument('--private-key', help='Private key file for digital signature')
    hide_parser.add_argument('--public-key', help='Public key file for RSA encryption')
    
    # Enhanced extract command
    extract_parser = subparsers.add_parser('extract', help='Extract data from stego image/video')
    extract_parser.add_argument('stego_file', help='Stego image/video path')
    extract_parser.add_argument('-p', '--password', required=True, help='Decryption password')
    extract_parser.add_argument('-o', '--output', help='Output file for extracted data')
    extract_parser.add_argument('--enhanced', action='store_true', help='Use enhanced security features')
    extract_parser.add_argument('--private-key', help='Private key file for RSA decryption')
    extract_parser.add_argument('--public-key', help='Public key file for signature verification')
    
    # Password strength checker
    pwd_parser = subparsers.add_parser('checkpwd', help='Check password strength')
    pwd_parser.add_argument('password', help='Password to check')
    
    # Key generation
    keys_parser = subparsers.add_parser('genkeys', help='Generate RSA key pair')
    keys_parser.add_argument('-o', '--output', default='keys', help='Output prefix for key files')
    
    # Capacity command
    capacity_parser = subparsers.add_parser('capacity', help='Check image/video capacity')
    capacity_parser.add_argument('file', help='Image/video path to analyze')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Determine if input is video or image
    def is_video(filepath):
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        return any(filepath.lower().endswith(ext) for ext in video_extensions)
    
    if args.command == 'checkpwd':
        enhanced_stego = EnhancedSteganography()
        score, strength, feedback = enhanced_stego.check_password_strength(args.password)
        print(f"Password Strength: {strength} ({score}/100)")
        if feedback:
            print("Recommendations:")
            for tip in feedback:
                print(f"  - {tip}")
    
    elif args.command == 'genkeys':
        enhanced_stego = EnhancedSteganography()
        private_key, public_key = enhanced_stego.generate_rsa_keys()
        
        private_file = f"{args.output}_private.pem"
        public_file = f"{args.output}_public.pem"
        
        with open(private_file, 'wb') as f:
            f.write(private_key)
        with open(public_file, 'wb') as f:
            f.write(public_key)
        
        print(f"SUCCESS: RSA key pair generated")
        print(f"Private key: {private_file}")
        print(f"Public key: {public_file}")
    
    elif args.command == 'hide':
        # Get secret data
        if args.data:
            secret_data = args.data
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    secret_data = f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            print("Error: Provide either --data or --file")
            return
        
        # Load keys if provided
        private_key_pem = None
        public_key_pem = None
        
        if args.private_key:
            try:
                with open(args.private_key, 'rb') as f:
                    private_key_pem = f.read()
            except Exception as e:
                print(f"Error loading private key: {e}")
                return
        
        if args.public_key:
            try:
                with open(args.public_key, 'rb') as f:
                    public_key_pem = f.read()
            except Exception as e:
                print(f"Error loading public key: {e}")
                return
        
        # Choose steganography method
        if is_video(args.input):
            stego = MinimalVideoSteganography()
            success, message = stego.hide_data_in_video(args.input, secret_data, args.password, args.output)
        elif args.enhanced or private_key_pem or public_key_pem:
            stego = EnhancedSteganography()
            success, message = stego.hide_data_enhanced(
                args.input, secret_data, args.password, args.output,
                private_key_pem, public_key_pem
            )
        else:
            stego = SecureSteganography()
            success, message = stego.hide_data(args.input, secret_data, args.password, args.output)
        
        if success:
            print(f"SUCCESS: {message}")
            print(f"Stego file saved: {args.output}")
            if private_key_pem:
                print("SUCCESS: Digital signature added")
            if public_key_pem:
                print("SUCCESS: RSA encryption applied")
            if args.enhanced:
                print("SUCCESS: Detection resistance enabled")
        else:
            print(f"ERROR: {message}")
    
    elif args.command == 'extract':
        # Load keys if provided
        private_key_pem = None
        public_key_pem = None
        
        if args.private_key:
            try:
                with open(args.private_key, 'rb') as f:
                    private_key_pem = f.read()
            except Exception as e:
                print(f"Error loading private key: {e}")
                return
        
        if args.public_key:
            try:
                with open(args.public_key, 'rb') as f:
                    public_key_pem = f.read()
            except Exception as e:
                print(f"Error loading public key: {e}")
                return
        
        # Choose extraction method
        if is_video(args.stego_file):
            stego = MinimalVideoSteganography()
            success, result = stego.extract_data_from_video(args.stego_file, args.password)
        elif args.enhanced or private_key_pem or public_key_pem:
            stego = EnhancedSteganography()
            success, result = stego.extract_data_enhanced(
                args.stego_file, args.password,
                private_key_pem, public_key_pem
            )
        else:
            stego = SecureSteganography()
            success, result = stego.extract_data(args.stego_file, args.password)
        
        if success:
            print("SUCCESS: Data extracted successfully!")
            
            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(result)
                    print(f"Extracted data saved to: {args.output}")
                except Exception as e:
                    print(f"Error saving to file: {e}")
                    print("Extracted data:")
                    print(result)
            else:
                print("Extracted data:")
                print(result)
        else:
            print(f"ERROR: {result}")
    
    elif args.command == 'capacity':
        import tempfile
        if is_video(args.file):
            stego = MinimalVideoSteganography()
            with tempfile.TemporaryDirectory() as temp_dir:
                first_frame = os.path.join(temp_dir, "frame.png")
                if stego.extract_first_frame(args.file, first_frame):
                    capacity = stego.get_image_capacity(first_frame)
                    print(f"Video: {args.file}")
                    print(f"Maximum capacity: {capacity} characters")
                    print(f"Equivalent to: ~{capacity/1024:.2f} KB of text")
                else:
                    print("Error: Could not analyze video")
        else:
            stego = SecureSteganography()
            capacity = stego.get_image_capacity(args.file)
            if capacity > 0:
                print(f"Image: {args.file}")
                print(f"Maximum capacity: {capacity} characters")
                print(f"Equivalent to: ~{capacity/1024:.2f} KB of text")
            else:
                print("Error: Could not analyze image")

if __name__ == '__main__':
    main()