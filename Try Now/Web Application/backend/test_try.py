"""
test_tryon.py
Test the IDM-VTON backend directly from the command line.
No server needed — runs the try-on function directly.

Usage:
    python test_tryon.py --person person.jpg --garment shirt.jpg
    python test_tryon.py --person person.jpg --garment shirt.jpg --desc "white cotton t-shirt"
"""

import argparse
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from tryon import run_upper_body_tryon


def main():
    parser = argparse.ArgumentParser(description="Test FitAI upper-body try-on")
    parser.add_argument("--person",  required=True, help="Path to person image")
    parser.add_argument("--garment", required=True, help="Path to garment image")
    parser.add_argument("--desc",    default="",    help="Garment description (optional)")
    parser.add_argument("--steps",   type=int, default=30, help="Denoising steps (default 30)")
    parser.add_argument("--seed",    type=int, default=42,  help="Seed (default 42)")
    parser.add_argument("--output",  default="result.png",  help="Output file path")
    args = parser.parse_args()

    # Check files exist
    for f, name in [(args.person, "person"), (args.garment, "garment")]:
        if not os.path.exists(f):
            print(f"❌  {name} image not found: {f}")
            sys.exit(1)

    # Check HF token
    hf = os.environ.get("HF_TOKEN", "")
    groq = os.environ.get("GROQ_API_KEY", "")
    print(f"HF_TOKEN    : {'✓ SET' if hf   else '✗ NOT SET (limited quota)'}")
    print(f"GROQ_API_KEY: {'✓ SET' if groq else '✗ NOT SET'}")
    print()
    print(f"Person   : {args.person}")
    print(f"Garment  : {args.garment}")
    print(f"Desc     : '{args.desc}'")
    print(f"Steps    : {args.steps}")
    print(f"Seed     : {args.seed}")
    print(f"Output   : {args.output}")
    print()
    print("Running try-on...")

    with open(args.person,  "rb") as f: person_bytes  = f.read()
    with open(args.garment, "rb") as f: garment_bytes = f.read()

    try:
        result = run_upper_body_tryon(
            person_bytes=person_bytes,
            garment_bytes=garment_bytes,
            garment_description=args.desc,
            denoise_steps=args.steps,
            seed=args.seed,
        )

        result.result_img.save(args.output)
        print(f"✅  Done! Result saved to: {args.output}")
        print(f"    Result size: {result.result_img.size[0]}x{result.result_img.size[1]} px")

    except Exception as e:
        print(f"❌  Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()