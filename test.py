from huggingface_hub import SpaceCardData, SpaceCard

print(SpaceCardData(title="hello"))

print(SpaceCard.from_template(SpaceCardData(title="hello")).save("README.md"))

from huggingface_hub import SpaceCardData

# Create metadata for your Space
card_data = SpaceCardData(
    title="My Cool Space",
    sdk="gradio",  # or "streamlit", "docker", or "static"
    license="mit",
    models=["distilbert-base-uncased"],
    datasets=["imdb"],
)

from huggingface_hub import SpaceCard

# Create the content for the card using the SpaceCardData
card_content = f"""
---
title: {card_data.title}
sdk: {card_data.sdk}
license: {card_data.license}
models: {card_data.models}
datasets: {card_data.datasets}
---

# Welcome to {card_data.title}!

This space uses the {card_data.sdk} SDK.
"""
card = SpaceCard(card_content)

card.save("README.md")
