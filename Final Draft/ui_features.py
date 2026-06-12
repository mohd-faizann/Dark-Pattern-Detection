"""HTML-based UI feature extraction for dark pattern signals."""

from bs4 import BeautifulSoup


class UIFeatureExtractor:
    MISLEADING_BUTTON_PHRASES = [
        "continue",
        "yes",
        "get started",
        "accept all",
        "agree",
    ]

    SUBSCRIPTION_PHRASES = [
        "subscribe",
        "subscription",
        "free trial",
        "auto-renew",
        "recurring",
    ]

    CANCELLATION_PHRASES = [
        "cancel subscription",
        "unsubscribe",
        "manage subscription",
        "cancel membership",
    ]

    def extract(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")
        page_text = soup.get_text(separator=" ", strip=True).lower()

        popups = soup.find_all(
            class_=lambda c: c and "popup" in str(c).lower()
        )
        popups += soup.find_all(
            id=lambda i: i and "popup" in str(i).lower()
        )
        popups += soup.find_all(
            attrs={"role": "dialog"}
        )

        checkboxes = soup.find_all("input", {"type": "checkbox"})
        prechecked = [box for box in checkboxes if box.has_attr("checked")]

        buttons = soup.find_all(["button", "a", "input"])
        misleading_buttons = 0
        for btn in buttons:
            label = (
                btn.get_text(strip=True)
                or btn.get("value", "")
                or btn.get("aria-label", "")
            ).lower()
            if any(phrase in label for phrase in self.MISLEADING_BUTTON_PHRASES):
                misleading_buttons += 1

        subscription_traps = sum(
            page_text.count(phrase) for phrase in self.SUBSCRIPTION_PHRASES
        )

        hidden_cancellation = sum(
            1 for phrase in self.CANCELLATION_PHRASES if phrase in page_text
        )
        # Hidden if cancellation wording exists but is buried in fine print
        if hidden_cancellation and "terms" in page_text:
            hidden_cancellation += 1

        return {
            "popup_count": len(popups),
            "prechecked_boxes": len(prechecked),
            "misleading_buttons": misleading_buttons,
            "subscription_traps": subscription_traps,
            "hidden_cancellation_paths": hidden_cancellation,
        }
