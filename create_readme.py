import argparse
import yaml
from pathlib import Path


# Define CLI arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a Space README.md and save it locally."
    )

    # Space configuration parameters
    parser.add_argument("--title", type=str, required=True, help="Title of the space.")
    parser.add_argument("--emoji", type=str, help="Emoji for the space.")
    parser.add_argument(
        "--color_from",
        type=str,
        choices=["red", "yellow", "green", "blue", "indigo", "purple", "pink", "gray"],
        help="Starting color of thumbnail gradient.",
    )
    parser.add_argument(
        "--color_to",
        type=str,
        choices=["red", "yellow", "green", "blue", "indigo", "purple", "pink", "gray"],
        help="Ending color of thumbnail gradient.",
    )
    parser.add_argument(
        "--sdk",
        type=str,
        choices=["gradio", "streamlit", "docker", "static"],
        required=True,
        help="SDK to use for the space.",
    )
    parser.add_argument(
        "--python_version",
        type=str,
        default="3.10",
        help="Python version (default: 3.10).",
    )
    parser.add_argument("--sdk_version", type=str, help="Version of the selected SDK.")
    parser.add_argument(
        "--suggested_hardware",
        type=str,
        help="Suggested hardware (e.g., 'cpu-basic', 't4-small').",
    )
    parser.add_argument(
        "--suggested_storage",
        type=str,
        choices=["small", "medium", "large"],
        help="Suggested storage for the space.",
    )
    parser.add_argument(
        "--app_file", type=str, required=True, help="Path to the main application file."
    )
    parser.add_argument(
        "--app_port", type=int, help="Port number (only for docker SDK)."
    )
    parser.add_argument(
        "--base_path", type=str, help="Initial URL to render (for non-static spaces)."
    )
    parser.add_argument(
        "--full_width",
        action="store_true",
        help="Render space in full-width inside iframe.",
    )
    parser.add_argument(
        "--header",
        type=str,
        choices=["mini", "default"],
        help="Header type (mini or default).",
    )
    parser.add_argument(
        "--short_description", type=str, help="Short description for the space."
    )
    parser.add_argument(
        "--models", nargs="+", help="List of model IDs used in the space."
    )
    parser.add_argument(
        "--datasets", nargs="+", help="List of dataset IDs used in the space."
    )
    parser.add_argument("--tags", nargs="+", help="List of tags describing the space.")
    parser.add_argument("--thumbnail", type=str, help="URL for a custom thumbnail.")
    parser.add_argument(
        "--pinned", action="store_true", help="Pin the space on top of your profile."
    )
    parser.add_argument(
        "--hf_oauth", action="store_true", help="Enable OAuth for the space."
    )
    parser.add_argument(
        "--hf_oauth_scopes",
        nargs="+",
        help="Authorized OAuth scopes for the connected app.",
    )
    parser.add_argument(
        "--hf_oauth_expiration_minutes",
        type=int,
        help="Duration of OAuth token in minutes.",
    )
    parser.add_argument(
        "--disable_embedding",
        action="store_true",
        help="Disable embedding of the space in other websites.",
    )
    parser.add_argument(
        "--startup_duration_timeout",
        type=str,
        help="Set custom startup duration timeout (e.g., '1h', '30m').",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="Directory to save the README.md file (default: current directory).",
    )

    return parser.parse_args()


# Create the content for the README.md
def create_readme_content(args):
    # Create the metadata dictionary
    card_data = {
        "title": args.title,
        "emoji": args.emoji,
        "colorFrom": args.color_from,
        "colorTo": args.color_to,
        "sdk": args.sdk,
        "python_version": args.python_version,
        "sdk_version": args.sdk_version,
        "suggested_hardware": args.suggested_hardware,
        "suggested_storage": args.suggested_storage,
        "app_file": args.app_file,
        "app_port": args.app_port,
        "base_path": args.base_path,
        "fullWidth": args.full_width,
        "header": args.header,
        "short_description": args.short_description,
        "models": args.models if args.models else [],
        "datasets": args.datasets if args.datasets else [],
        "tags": args.tags if args.tags else [],
        "thumbnail": args.thumbnail,
        "pinned": args.pinned,
        "hf_oauth": args.hf_oauth,
        "hf_oauth_scopes": args.hf_oauth_scopes,
        "hf_oauth_expiration_minutes": args.hf_oauth_expiration_minutes,
        "disable_embedding": args.disable_embedding,
        "startup_duration_timeout": args.startup_duration_timeout,
    }

    # Filter out None values from the dictionary
    card_data = {key: value for key, value in card_data.items() if value is not None}

    # Convert dictionary to YAML block
    yaml_content = yaml.dump(card_data, sort_keys=False)

    # Add the YAML block and a placeholder for the README content
    readme_content = f"---\n{yaml_content}---\n\n# {args.title}\n\nThis is the README for the space: {args.title}."

    return readme_content


# Save README.md to the specified directory
def save_readme(readme_content, output_dir):
    output_path = Path(output_dir) / "README.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"README.md saved to {output_path}")


# Main execution
if __name__ == "__main__":
    args = parse_args()
    readme_content = create_readme_content(args)
    save_readme(readme_content, args.output_dir)
