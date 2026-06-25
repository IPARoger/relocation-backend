"""Stub AI summary provider — structured JSON text only, no OpenAI wiring."""

from __future__ import annotations

_FIELDS = (
    "overview",
    "population",
    "climate",
    "cost",
    "safety",
    "language",
    "healthcare",
    "transport",
    "visa",
    "culture",
    "expat",
)

_STUB_VERSION = "ci-stub-v1"


def _pad_to_band(text: str, target: int = 62) -> str:
    words = text.split()
    if len(words) >= 50:
        return text
    filler = (
        "Relocators should validate these baseline notes against current local sources, "
        "recent policy changes, and personal chart priorities before making long-term commitments. "
        "This stub supplies structured placeholder context for engineering and UI integration only."
    )
    combined = text + " " + filler
    words = combined.split()
    return " ".join(words[: max(50, min(target, 80))])


class AiSummaryProvider:
    """Returns ~50-80 word placeholder prose per field for development."""

    version = _STUB_VERSION

    def generate_summaries(
        self,
        *,
        place: dict,
        location_context: dict | None,
        airports: dict,
        photos: dict,
    ) -> dict[str, str]:
        ctx = location_context or {}
        name = place.get("display_name") or ctx.get("suggested_name") or "this location"
        country = place.get("country_name") or ctx.get("country_name") or "the region"
        regional = ctx.get("regional_context") or name
        remote_note = ""
        if ctx.get("is_remote"):
            remote_note = (
                f" Figures below use {regional} as regional context; "
                "wilderness-specific statistics are not invented for remote coordinates."
            )
        pop = place.get("population")
        pop_hint = f"approximately {pop:,} residents" if pop else "a mid-sized urban population"

        templates = {
            "overview": (
                f"{name} in {country} offers a distinctive relocation profile combining local character, "
                f"practical infrastructure, and everyday livability factors worth weighing alongside chart work. "
                f"This overview summarizes baseline context for decision support, not travel marketing. "
                f"Neighborhood texture, commute patterns, and seasonal rhythms all influence how a chart "
                f"experience translates into daily life for long-stay visitors and permanent movers alike.{remote_note}"
            ),
            "population": (
                f"The greater {name} area supports {pop_hint}, with central districts denser than outer suburbs. "
                f"Growth has been steady rather than explosive, shaping housing supply, commute patterns, and the depth of local services. "
                f"Age distribution skews toward working adults in core districts, while family-oriented suburbs retain stronger school catchments. "
                f"Demographic inflows include domestic migrants, international professionals, and retirees seeking milder climates or lower costs."
            ),
            "climate": (
                f"{name} experiences seasonal variation typical of its latitude in {country}, with warmer summers, "
                f"milder shoulder seasons, and a rainy period that rewards planning for humidity or dry heat depending on exposure. "
                f"Coastal neighborhoods often feel breezier than inland districts, and elevation can shift temperatures noticeably within the metro. "
                f"Pack for layered weather, especially if you plan frequent regional travel or outdoor work across multiple microclimates."
            ),
            "cost": (
                f"Day-to-day costs in {name} sit near the national median for housing, groceries, and utilities, "
                f"though central neighborhoods command premiums. Remote workers should budget for transport and healthcare outliers. "
                f"Renters face deposit norms and agency fees that vary by district, while owners encounter property taxes and maintenance norms "
                f"that differ from North American expectations. Dining out ranges from affordable local canteens to international-priced fine dining."
            ),
            "safety": (
                f"Personal safety in {name} is generally comparable to other cities of its size in {country}, "
                f"with ordinary urban precautions advised in transit hubs and nightlife districts after dark. "
                f"Property crime in tourist zones warrants standard vigilance with bags and phones, while violent crime rates remain moderate "
                f"relative to global peers. Emergency services are reachable by national short codes; response times are fastest in central wards."
            ),
            "language": (
                f"The dominant language in {name} is the national language of {country}, with English increasingly "
                f"available in services, expat neighborhoods, and professional settings though not guaranteed everywhere. "
                f"Government paperwork may require certified translations, and phone support is not always bilingual. "
                f"Even modest language study improves housing negotiations, healthcare intake, and everyday errands outside international enclaves."
            ),
            "healthcare": (
                f"Healthcare access in {name} includes public facilities and private clinics; wait times and costs vary by residency status. "
                f"Specialists concentrate in larger districts, so suburban relocators should confirm proximity to preferred providers. "
                f"Pharmacies are widely available for routine needs, while dental and vision care are often private-pay unless insured. "
                f"Travelers should carry prescriptions in original packaging and confirm reciprocity agreements before assuming coverage."
            ),
            "transport": (
                f"Getting around {name} relies on a mix of metro, bus, rideshare, and walkable cores in older districts. "
                f"Car ownership is optional in central areas but useful for outer suburbs and regional day trips. "
                f"Commuter rail links may serve satellite towns, and bike lanes are expanding though not uniform citywide. "
                f"Airport connections typically require a transfer unless you choose taxi or private shuttle service from central hubs."
            ),
            "visa": (
                f"Visa and residency rules for {country} depend on nationality, employment, and length of stay; "
                f"{name} follows national immigration policy without a separate municipal scheme. Professional advice is recommended before relocating. "
                f"Short-stay visitors may enter under visa-waiver or Schengen-style limits, while workers need employer sponsorship or freelancer pathways "
                f"where available. Tax residency thresholds differ from immigration stamps and should be reviewed with qualified counsel."
            ),
            "culture": (
                f"Cultural life in {name} blends historic architecture, local food traditions, and contemporary arts scenes. "
                f"Festivals and neighborhood markets provide accessible entry points for newcomers exploring daily rhythms. "
                f"Museums, live music venues, and weekend street events cluster in walkable cores, while suburban malls serve practical shopping. "
                f"Respect for local customs around meals, greetings, and quiet hours helps integration more than tourism-oriented checklist sightseeing."
            ),
            "expat": (
                f"Expat communities in {name} cluster in walkable districts with international schools, coworking spaces, and English-friendly services. "
                f"Integration is smoother with basic language effort and participation in local clubs or professional networks. "
                f"Online groups coordinate housing leads and bureaucratic tips, though scams exist in rental markets aimed at newcomers. "
                f"Long-term residents report that balancing expat comfort with local friendships yields the most stable relocation experience."
            ),
        }
        return {field: _pad_to_band(templates[field]) for field in _FIELDS}
