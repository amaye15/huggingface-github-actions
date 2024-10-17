#!/usr/bin/env python3

import argparse
from huggingface_hub import HfApi, HfFolder
from huggingface_hub.utils import RepositoryNotFoundError
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Check if a Hugging Face Space exists, and create it if not."
    )
    parser.add_argument(
        "--token",
        "-t",
        help="Hugging Face API token. Can also be set via the HF_API_TOKEN environment variable.",
    )
    parser.add_argument(
        "--space-name",
        "-n",
        required=True,
        help="Name of the space to check or create.",
    )
    parser.add_argument(
        "--sdk",
        "-s",
        choices=["gradio", "streamlit", "static", "docker"],
        default="gradio",
        help="SDK type for the space (default: gradio).",
    )
    parser.add_argument(
        "--private", "-p", action="store_true", help="Create the space as private."
    )
    parser.add_argument(
        "--org", "-o", help="Organization under which to create the space."
    )

    args = parser.parse_args()

    # Get the API token (from argument, environment variable, or fail)
    api_token = args.token or os.getenv("HF_API_TOKEN")
    if api_token is None:
        print(
            "Error: Hugging Face API token must be provided via --token argument or HF_API_TOKEN environment variable."
        )
        sys.exit(1)

    # Save the token so that HfApi can use it
    HfFolder.save_token(api_token)

    api = HfApi(token=api_token)

    space_name = args.space_name

    # Determine the repository owner (user or organization)
    if args.org:
        owner = args.org
    else:
        # Retrieve your username from the token
        try:
            user_info = api.whoami()
            owner = user_info["name"]
        except Exception as e:
            print(f"Failed to retrieve user information: {e}")
            sys.exit(1)

    full_repo_name = f"{owner}/{space_name}"

    # Check if the space exists
    try:
        repo_info = api.repo_info(repo_id=full_repo_name, repo_type="space")
        print(f"Space '{full_repo_name}' already exists.")
    except RepositoryNotFoundError:
        print(f"Space '{full_repo_name}' does not exist. Creating it...")
        # Create the new space
        try:
            api.create_repo(
                repo_id=space_name,
                repo_type="space",
                space_sdk=args.sdk,
                private=args.private,
                # organization=args.org,
            )
            print(f"Space '{full_repo_name}' has been created with SDK '{args.sdk}'.")
        except Exception as e:
            print(f"Failed to create space '{full_repo_name}': {e}")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while checking the space: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
