"""based on their chat template"""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar
from webui.state import State


def index() -> rx.Component:
    return rx.chakra.vstack(
        navbar(),
        rx.chakra.text("Built and hosted with Reflex.dev", text_align="center", font_size = "2em"), 
        rx.chakra.text("Under the hood: recipe-fine-tuned Mistral-7b and an AI Agent that creates recipes, searches for the cheapest ingredients near you, makes a detailed shopping list, and purchases the ingredients using Instacart API.", text_align="center", font_size = "1em"),
        rx.chakra.text("Say 'get me' + a creative food to trigger the agent.", text_align="center", font_size = "1em"),  
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


app = rx.App(style=styles.base_style)
app.add_page(index)
