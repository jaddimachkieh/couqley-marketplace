"""
Menu Engineering Analyzer for Couqley.
Boston Matrix classification, Challenge item marketing plays, profit optimization.
Self-contained — no imports from other couqley skills.

Data Source: Menu engineering DataFrame from parse_menu_engineering_csv()
This contains menu items with categories (Star, Challenge, Workhorse, Dog),
profit margins, popularity, quantities, prices, and groupings.

Generates:
1. Marketing plays for top Challenge items (high margin, low volume)
2. Menu Engineering Matrix analysis (2x2 quadrant visualization)
3. Profit optimization scenarios (what-if analysis)
4. Social media hooks, server scripts, pricing strategies, bundle suggestions
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Column helpers — work with Menu Engineering columns
# ---------------------------------------------------------------------------

def _name_col(df: pd.DataFrame) -> Optional[str]:
    """Return the item name column present in df."""
    for c in ['menu_item', 'item_name']:
        if c in df.columns:
            return c
    return None


def _revenue_col(df: pd.DataFrame) -> Optional[str]:
    """Return the revenue column present in df."""
    for c in ['total_revenue', 'total_amount']:
        if c in df.columns:
            return c
    return None


def _qty_col(df: pd.DataFrame) -> Optional[str]:
    for c in ['quantity']:
        if c in df.columns:
            return c
    return None


def _group_col(df: pd.DataFrame) -> Optional[str]:
    for c in ['group']:
        if c in df.columns:
            return c
    return None


# ---------------------------------------------------------------------------
# Core Menu Engineering Functions
# ---------------------------------------------------------------------------

def menu_marketing_engine(
    menu_df: pd.DataFrame,
    top_n: int = 20
) -> Dict[str, Any]:
    """
    Generate marketing plays for Challenge items (high margin, low volume).

    Takes a DataFrame directly (output of parse_menu_engineering_csv) and generates:
    - Top N marketing plays with action plans, bundles, pricing strategies
    - Menu Engineering Matrix (quadrant analysis)
    - Profit optimization scenarios (what-if analysis)

    Args:
        menu_df: DataFrame with columns:
            - menu_item, category, quantity, popularity, item_cost, item_sell_price,
            - item_profit, total_cost, total_revenue, total_profit, profit_margin_pct,
            - profit_margin, popularity_level, menu, group
        top_n: Number of top items to generate plays for (default: 20)

    Returns:
        JSON-serializable dict with:
        - challenge_items: All Challenge items with metrics
        - marketing_plays: Top N actionable marketing plays
        - menu_engineering_matrix: Matrix analysis with quadrants
        - profit_optimization: What-if scenario analysis
        - summary: Statistics and insights
        - summary_text: Human-readable summary
        - insights: Quick LLM-friendly summaries
    """
    # Get menu engineering data
    menu_df_copy = menu_df.copy()

    if menu_df_copy.empty:
        return {
            "challenge_items": [],
            "marketing_plays": [],
            "menu_engineering_matrix": {
                "matrix_data": [],
                "quadrants": {},
                "quadrant_statistics": {},
                "recommendations": {},
                "summary": {"total_items": 0}
            },
            "profit_optimization": {
                "scenarios": [],
                "summary": {
                    "total_items_analyzed": 0,
                    "current_total_profit": 0.0,
                    "projected_total_profit": 0.0,
                    "profit_increase": 0.0,
                    "profit_increase_pct": 0.0
                },
                "top_opportunities": []
            },
            "summary": {
                "total_challenge_items": 0,
                "top_n_items": 0,
                "total_current_revenue": 0.0,
                "total_current_profit": 0.0,
                "currency": "USD"
            },
            "summary_text": "No menu engineering data available."
        }

    # Filter for Challenge items only
    challenge_items = menu_df_copy[menu_df_copy['category'] == 'Challenge'].copy()

    if challenge_items.empty:
        return {
            "challenge_items": [],
            "marketing_plays": [],
            "menu_engineering_matrix": generate_menu_engineering_matrix(menu_df_copy),
            "profit_optimization": calculate_profit_optimization(menu_df_copy, volume_increase_pct=30.0),
            "summary": {
                "total_challenge_items": 0,
                "top_n_items": 0,
                "total_current_revenue": 0.0,
                "total_current_profit": 0.0,
                "currency": "USD"
            },
            "summary_text": "No Challenge items found in the menu engineering data."
        }

    # Sort by potential (profit margin * current revenue opportunity)
    challenge_items['potential_score'] = (
        challenge_items['profit_margin_pct'] * challenge_items['total_profit']
    )
    challenge_items = challenge_items.sort_values('potential_score', ascending=False)

    # Keep only top N items for marketing plays
    total_challenge_items = len(challenge_items)
    top_challenge_items = challenge_items.head(top_n).copy()

    # Generate marketing plays for top challenge items only
    marketing_plays = []

    for idx, item in top_challenge_items.iterrows():
        play = generate_play_for_item(item, challenge_items)
        marketing_plays.append(play)

    # Calculate summary statistics
    total_potential_revenue = challenge_items['total_revenue'].sum()
    total_potential_profit = challenge_items['total_profit'].sum()
    avg_profit_margin = challenge_items['profit_margin_pct'].mean()
    avg_quantity = challenge_items['quantity'].mean()

    # Group by category for insights
    by_group = challenge_items.groupby('group').agg({
        'quantity': 'sum',
        'total_revenue': 'sum',
        'total_profit': 'sum',
        'profit_margin_pct': 'mean'
    }).round(2)

    top_groups = by_group.sort_values('total_profit', ascending=False).head(5)

    # Calculate top N statistics
    top_n_revenue = top_challenge_items['total_revenue'].sum()
    top_n_profit = top_challenge_items['total_profit'].sum()

    # Generate human-readable summary
    summary_parts = [
        f"Found {total_challenge_items} Challenge items (high margin, low volume) requiring marketing attention."
    ]
    summary_parts.append(
        f"Focusing on top {top_n} items by potential score (profit margin × total profit)."
    )
    summary_parts.append(
        f"Top {top_n} items represent ${top_n_revenue:,.2f} revenue "
        f"(${top_n_profit:,.2f} profit) out of ${total_potential_revenue:,.2f} total."
    )
    summary_parts.append(
        f"Average profit margin: {avg_profit_margin:.1f}% with average quantity of {avg_quantity:.1f} units."
    )
    if len(top_groups) > 0:
        summary_parts.append(
            f"Top group by profit: {top_groups.index[0]} "
            f"with ${top_groups['total_profit'].iloc[0]:,.2f} profit."
        )
    summary_parts.append(
        f"Generated {len(marketing_plays)} actionable marketing plays for top priority items."
    )

    summary_text = " ".join(summary_parts)

    # Convert top challenge items to records for JSON
    challenge_items_records = challenge_items.to_dict('records')
    # Mark which items are in the top N
    top_n_indices = set(top_challenge_items.index)
    for record in challenge_items_records:
        record['in_top_n'] = record.get('menu_item') in top_challenge_items['menu_item'].values

    # Convert numpy types to native Python types
    for record in challenge_items_records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, (float, int)):
                record[key] = round(float(value), 2)
            else:
                record[key] = str(value)

    # Generate Menu Engineering Matrix
    matrix_analysis = generate_menu_engineering_matrix(menu_df_copy)

    # Generate Profit Optimization scenarios (30% volume increase for Challenge items)
    profit_optimization = calculate_profit_optimization(menu_df_copy, volume_increase_pct=30.0)

    return {
        "challenge_items": challenge_items_records,
        "marketing_plays": marketing_plays,
        "menu_engineering_matrix": matrix_analysis,
        "profit_optimization": profit_optimization,
        "summary": {
            "total_challenge_items": total_challenge_items,
            "top_n_items": top_n,
            "top_n_revenue": round(top_n_revenue, 2),
            "top_n_profit": round(top_n_profit, 2),
            "total_current_revenue": round(total_potential_revenue, 2),
            "total_current_profit": round(total_potential_profit, 2),
            "avg_profit_margin_pct": round(avg_profit_margin, 2),
            "avg_quantity": round(avg_quantity, 2),
            "top_groups": [
                {
                    "group": str(group_name),
                    "total_profit": round(float(row['total_profit']), 2),
                    "total_revenue": round(float(row['total_revenue']), 2),
                    "quantity": round(float(row['quantity']), 2),
                    "avg_profit_margin_pct": round(float(row['profit_margin_pct']), 2)
                }
                for group_name, row in top_groups.iterrows()
            ],
            "currency": "USD"
        },
        "summary_text": summary_text,
        "insights": {
            "matrix_summary": (
                f"Menu Engineering Matrix: {matrix_analysis['summary']['stars_count']} Stars, "
                f"{matrix_analysis['summary']['challenges_count']} Challenges, "
                f"{matrix_analysis['summary']['workhorses_count']} Workhorses, "
                f"{matrix_analysis['summary']['dogs_count']} Dogs. "
                f"Focus marketing on {matrix_analysis['summary']['challenges_count']} Challenge items."
            ),
            "profit_optimization_summary": profit_optimization.get('summary_text', '')
        }
    }


def generate_play_for_item(item: pd.Series, all_challenge_items: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a specific marketing play for a Challenge item.

    Args:
        item: Series representing a single menu item
        all_challenge_items: DataFrame of all challenge items for context

    Returns:
        Dict with action plan, bundle suggestions, pricing strategy, social media hooks, server scripts
    """
    menu_item = str(item['menu_item'])
    group = str(item.get('group', 'Unknown'))
    profit_margin_pct = float(item['profit_margin_pct'])
    quantity = float(item['quantity'])
    item_sell_price = float(item['item_sell_price'])
    item_profit = float(item['item_profit'])

    # Determine action plan based on item characteristics
    action_plan = determine_action_plan(item, all_challenge_items)

    # Generate bundle suggestions
    bundle_suggestions = generate_bundle_suggestions(item, all_challenge_items)

    # Generate pricing strategy
    pricing_strategy = generate_pricing_strategy(item)

    # Generate social media hooks
    social_media_hooks = generate_social_media_hooks(item)

    # Generate server scripts
    server_scripts = generate_server_scripts(item)

    return {
        "menu_item": menu_item,
        "group": group,
        "current_metrics": {
            "quantity": round(quantity, 2),
            "item_sell_price": round(item_sell_price, 2),
            "item_profit": round(item_profit, 2),
            "profit_margin_pct": round(profit_margin_pct, 2),
            "total_revenue": round(float(item['total_revenue']), 2),
            "total_profit": round(float(item['total_profit']), 2)
        },
        "action_plan": action_plan,
        "bundle_suggestions": bundle_suggestions,
        "pricing_strategy": pricing_strategy,
        "social_media_hooks": social_media_hooks,
        "server_scripts": server_scripts,
        "priority": "high" if profit_margin_pct > 60 else "medium"
    }


def determine_action_plan(item: pd.Series, all_challenge_items: pd.DataFrame) -> Dict[str, Any]:
    """
    Determine the primary action plan for a Challenge item.

    Strategy is based on:
    - Very low volume + high margin: awareness and education
    - Low volume + high margin: premium positioning
    - Otherwise: volume boost

    Includes item-specific tactics for wines, cocktails, and steaks.
    """
    menu_item = str(item['menu_item']).lower()
    profit_margin_pct = float(item['profit_margin_pct'])
    quantity = float(item['quantity'])

    # Determine primary strategy
    if quantity < 5:
        primary_strategy = "awareness_and_education"
        tactics = [
            "Feature prominently on menu with descriptive callout",
            "Train servers to recommend and describe the item",
            "Create visual content showcasing the item"
        ]
    elif profit_margin_pct > 70:
        primary_strategy = "premium_positioning"
        tactics = [
            "Position as signature/premium item",
            "Bundle with popular items at slight discount",
            "Create limited-time offer or special"
        ]
    else:
        primary_strategy = "volume_boost"
        tactics = [
            "Bundle with high-volume items",
            "Offer as add-on or upgrade",
            "Create happy hour or time-based promotion"
        ]

    # Add item-specific tactics
    if any(word in menu_item for word in ['wine', 'carafe', 'bottle']):
        tactics.append("Suggest wine pairings with popular dishes")
        tactics.append("Offer by-the-glass specials to introduce bottle options")

    if any(word in menu_item for word in ['cocktail', 'martini', 'spritz']):
        tactics.append("Feature in happy hour promotion")
        tactics.append("Create Instagram-worthy presentation")
        tactics.append("Train bartenders to upsell during peak hours")

    if any(word in menu_item for word in ['steak', 'beef', 'boeuf', 'filet']):
        tactics.append("Position as premium protein option")
        tactics.append("Bundle with wine for date night special")
        tactics.append("Feature in weekend special promotions")

    return {
        "primary_strategy": primary_strategy,
        "tactics": tactics,
        "expected_impact": "Increase volume by 30-50% within 30 days",
        "implementation_timeframe": "1-2 weeks"
    }


def generate_bundle_suggestions(item: pd.Series, all_challenge_items: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Generate bundle suggestions for a Challenge item.

    Includes pairings for wines, cocktails, premium items, and generic bundles.
    """
    menu_item = str(item['menu_item'])
    item_price = float(item['item_sell_price'])
    group = str(item.get('group', ''))

    bundles = []

    # For wines, suggest pairing with popular dishes
    if any(word in menu_item.lower() for word in ['wine', 'carafe', 'bottle']):
        bundles.append({
            "bundle_name": f"{menu_item} + Popular Entree",
            "description": f"Pair {menu_item} with a popular entree at 15% discount",
            "bundle_price": round(item_price * 0.85 + 20, 2),
            "discount_pct": 15,
            "target_audience": "Date night diners, wine enthusiasts"
        })

    # For cocktails, suggest happy hour bundles
    if any(word in menu_item.lower() for word in ['cocktail', 'martini', 'spritz']):
        bundles.append({
            "bundle_name": f"{menu_item} + Appetizer",
            "description": f"Happy hour special: {menu_item} with select appetizer",
            "bundle_price": round(item_price * 0.9 + 12, 2),
            "discount_pct": 10,
            "target_audience": "After-work crowd, social diners"
        })

    # For premium items, suggest upgrade bundles
    if float(item['profit_margin_pct']) > 60:
        bundles.append({
            "bundle_name": f"Premium Experience: {menu_item}",
            "description": f"Upgrade your meal with {menu_item} - add for ${item_price * 0.8:.2f}",
            "bundle_price": round(item_price * 0.8, 2),
            "discount_pct": 20,
            "target_audience": "Special occasion diners, premium seekers"
        })

    # Generic bundle if no specific match
    if not bundles:
        bundles.append({
            "bundle_name": f"{menu_item} Discovery Bundle",
            "description": f"Try {menu_item} with a popular item - 10% off",
            "bundle_price": round(item_price * 0.9 + 15, 2),
            "discount_pct": 10,
            "target_audience": "Adventurous diners, value seekers"
        })

    return bundles


def generate_pricing_strategy(item: pd.Series) -> Dict[str, Any]:
    """
    Generate pricing strategy recommendations.

    Three strategies:
    - slight_price_reduction: Very low volume, very high margin
    - maintain_price_add_value: Low volume, good margin
    - promotional_pricing: Standard challenge items
    """
    current_price = float(item['item_sell_price'])
    profit_margin_pct = float(item['profit_margin_pct'])
    quantity = float(item['quantity'])

    # Pricing recommendations
    if quantity < 3 and profit_margin_pct > 70:
        recommendation = "slight_price_reduction"
        suggested_price = round(current_price * 0.95, 2)
        rationale = "High margin allows for 5% price reduction to drive volume without significant profit impact"
    elif quantity < 10 and profit_margin_pct > 50:
        recommendation = "maintain_price_add_value"
        suggested_price = current_price
        rationale = "Maintain current price but enhance perceived value through presentation and bundling"
    else:
        recommendation = "promotional_pricing"
        suggested_price = round(current_price * 0.90, 2)
        rationale = "Use limited-time promotional pricing to drive trial and volume"

    return {
        "current_price": round(current_price, 2),
        "recommendation": recommendation,
        "suggested_price": suggested_price,
        "price_change_pct": round((suggested_price - current_price) / current_price * 100, 1),
        "rationale": rationale,
        "implementation": "Test for 2 weeks, measure volume impact, adjust if needed"
    }


def generate_social_media_hooks(item: pd.Series) -> List[Dict[str, Any]]:
    """
    Generate Instagram/social media content hooks for the item.

    Includes captions, hashtags, story ideas, and visual suggestions.
    """
    menu_item = str(item['menu_item'])
    group = str(item.get('group', ''))

    hooks = []

    # Instagram caption ideas
    if any(word in menu_item.lower() for word in ['wine', 'carafe']):
        hooks.append({
            "platform": "Instagram",
            "hook_type": "caption",
            "content": f"Discover {menu_item} - A hidden gem on our menu! Perfect for pairing with your favorite dish. Ask your server for recommendations! #WineWednesday #RestaurantLife",
            "hashtags": ["#WineWednesday", "#RestaurantLife", "#FoodPairing", "#HiddenGem"],
            "visual_suggestion": "Wine bottle with food pairing, styled flat lay"
        })

    if any(word in menu_item.lower() for word in ['cocktail', 'martini']):
        hooks.append({
            "platform": "Instagram",
            "hook_type": "caption",
            "content": f"{menu_item} - Crafted with care, served with style. The perfect way to start your evening! Available during happy hour. #CocktailHour #CraftCocktails",
            "hashtags": ["#CocktailHour", "#CraftCocktails", "#HappyHour", "#Mixology"],
            "visual_suggestion": "Cocktail with garnish, backlit, professional photography"
        })

    if any(word in menu_item.lower() for word in ['steak', 'beef', 'filet']):
        hooks.append({
            "platform": "Instagram",
            "hook_type": "caption",
            "content": f"{menu_item} - Premium quality, exceptional flavor. Our chef's recommendation for a special night out. Book your table! #SteakNight #DateNight",
            "hashtags": ["#SteakNight", "#DateNight", "#ChefRecommendation", "#PremiumDining"],
            "visual_suggestion": "Sizzling steak plated beautifully, close-up shot"
        })

    # Generic hook if no specific match
    if not hooks:
        hooks.append({
            "platform": "Instagram",
            "hook_type": "caption",
            "content": f"{menu_item} - A customer favorite that deserves more attention! High quality, great value. Try it on your next visit! #RestaurantFavorites #FoodDiscovery",
            "hashtags": ["#RestaurantFavorites", "#FoodDiscovery", "#HiddenGem", "#TrySomethingNew"],
            "visual_suggestion": "Professional food photography, styled presentation"
        })

    # Add story ideas
    hooks.append({
        "platform": "Instagram Stories",
        "hook_type": "story",
        "content": f"Behind the scenes: How we prepare {menu_item}",
        "visual_suggestion": "Short video of preparation or plating process"
    })

    return hooks


def generate_server_scripts(item: pd.Series) -> List[Dict[str, Any]]:
    """
    Generate server recommendation scripts.

    Includes initial contact, after-order, end-of-meal, and talking points.
    """
    menu_item = str(item['menu_item'])
    group = str(item.get('group', ''))
    profit_margin_pct = float(item['profit_margin_pct'])

    scripts = []

    # Opening script
    scripts.append({
        "timing": "initial_contact",
        "script": f"Have you tried our {menu_item}? It's one of our hidden gems - [brief description]. It pairs beautifully with [suggested pairing].",
        "tone": "enthusiastic, informative"
    })

    # Upsell script
    scripts.append({
        "timing": "after_main_order",
        "script": f"To complement your meal, I'd recommend our {menu_item}. It's a customer favorite and pairs perfectly with what you've ordered. Would you like to try it?",
        "tone": "suggestive, helpful"
    })

    # Closing script (if not ordered)
    scripts.append({
        "timing": "end_of_meal",
        "script": f"Next time you visit, I'd love to introduce you to our {menu_item}. It's something special we're really proud of.",
        "tone": "warm, inviting"
    })

    # Key talking points
    scripts.append({
        "timing": "talking_points",
        "points": [
            f"High quality ingredients in {menu_item}",
            f"Perfect for [occasion/meal type]",
            f"Pairs well with [complementary items]",
            f"Great value for the quality"
        ]
    })

    return scripts


def generate_menu_engineering_matrix(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate Menu Engineering Matrix visualization data.

    Creates a 2x2 matrix: Profit Margin (High/Low) vs Popularity (High/Low)

    Quadrants:
    - Stars: High Profit, High Popularity - protect and promote
    - Challenges: High Profit, Low Popularity - market aggressively
    - Workhorses: Low Profit, High Popularity - optimize margins
    - Dogs: Low Profit, Low Popularity - remove or reposition

    Args:
        df: DataFrame with menu engineering data

    Returns:
        JSON-serializable dict with matrix data, quadrant analysis, and recommendations
    """
    if df.empty:
        return {
            "matrix_data": [],
            "quadrants": {
                "stars": [],
                "challenges": [],
                "workhorses": [],
                "dogs": []
            },
            "quadrant_statistics": {},
            "thresholds": {},
            "recommendations": {},
            "summary": {
                "total_items": 0,
                "stars_count": 0,
                "challenges_count": 0,
                "workhorses_count": 0,
                "dogs_count": 0
            }
        }

    # Calculate thresholds for high/low
    median_profit_margin = df['profit_margin_pct'].median()
    median_popularity = df['popularity'].median()

    # Categorize items into quadrants
    matrix_data = []
    quadrants = {
        'stars': [],
        'challenges': [],
        'workhorses': [],
        'dogs': []
    }

    for idx, row in df.iterrows():
        profit_high = row['profit_margin_pct'] >= median_profit_margin
        popularity_high = row['popularity'] >= median_popularity

        # Determine quadrant
        if profit_high and popularity_high:
            quadrant = 'stars'
        elif profit_high and not popularity_high:
            quadrant = 'challenges'
        elif not profit_high and popularity_high:
            quadrant = 'workhorses'
        else:
            quadrant = 'dogs'

        item_data = {
            'menu_item': str(row['menu_item']),
            'group': str(row.get('group', 'Unknown')),
            'profit_margin_pct': round(float(row['profit_margin_pct']), 2),
            'popularity': round(float(row['popularity']), 2),
            'quantity': round(float(row['quantity']), 2),
            'item_sell_price': round(float(row['item_sell_price']), 2),
            'total_profit': round(float(row['total_profit']), 2),
            'total_revenue': round(float(row['total_revenue']), 2),
            'quadrant': quadrant,
            'category': str(row['category'])
        }

        matrix_data.append(item_data)
        quadrants[quadrant].append(item_data)

    # Calculate quadrant statistics
    quadrant_stats = {}
    for quadrant_name, items in quadrants.items():
        if items:
            quadrant_stats[quadrant_name] = {
                'count': len(items),
                'total_revenue': round(sum(item['total_revenue'] for item in items), 2),
                'total_profit': round(sum(item['total_profit'] for item in items), 2),
                'avg_profit_margin': round(sum(item['profit_margin_pct'] for item in items) / len(items), 2),
                'avg_popularity': round(sum(item['popularity'] for item in items) / len(items), 2)
            }
        else:
            quadrant_stats[quadrant_name] = {
                'count': 0,
                'total_revenue': 0.0,
                'total_profit': 0.0,
                'avg_profit_margin': 0.0,
                'avg_popularity': 0.0
            }

    # Generate recommendations for each quadrant
    recommendations = {
        'stars': {
            'strategy': 'Protect and promote',
            'actions': [
                'Maintain current pricing',
                'Feature prominently on menu',
                'Use as signature items in marketing',
                'Ensure consistent quality',
                'Consider slight price increases if demand is very high'
            ],
            'priority': 'high'
        },
        'challenges': {
            'strategy': 'Market aggressively',
            'actions': [
                'Create targeted marketing campaigns',
                'Bundle with popular items',
                'Train staff to recommend',
                'Feature in social media',
                'Consider promotional pricing to drive trial',
                'Position as premium/special items'
            ],
            'priority': 'high'
        },
        'workhorses': {
            'strategy': 'Maintain volume, optimize margin',
            'actions': [
                'Keep prices competitive',
                'Use as traffic builders',
                'Optimize costs if possible',
                'Bundle with higher-margin items',
                'Maintain quality to keep volume'
            ],
            'priority': 'medium'
        },
        'dogs': {
            'strategy': 'Remove or reposition',
            'actions': [
                'Consider removing from menu',
                'If keeping, try repositioning or rebranding',
                'Test price reduction to increase volume',
                'Bundle with popular items',
                'Use as loss leaders if strategic'
            ],
            'priority': 'low'
        }
    }

    return {
        'matrix_data': matrix_data,
        'quadrants': quadrants,
        'quadrant_statistics': quadrant_stats,
        'thresholds': {
            'median_profit_margin_pct': round(median_profit_margin, 2),
            'median_popularity': round(median_popularity, 4)
        },
        'recommendations': recommendations,
        'summary': {
            'total_items': len(df),
            'stars_count': len(quadrants['stars']),
            'challenges_count': len(quadrants['challenges']),
            'workhorses_count': len(quadrants['workhorses']),
            'dogs_count': len(quadrants['dogs'])
        }
    }


def calculate_profit_optimization(df: pd.DataFrame, volume_increase_pct: float = 30.0, focus_items: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Calculate profit optimization scenarios (what-if analysis).

    Simulates volume increases and calculates profit impact for Challenge items.

    Args:
        df: DataFrame with menu engineering data
        volume_increase_pct: Percentage increase in volume to simulate (default: 30%)
        focus_items: Optional list of menu items to focus on. If None, focuses on Challenge items.

    Returns:
        JSON-serializable dict with scenario analysis and profit projections
    """
    # Focus on Challenge items by default, or specified items
    if focus_items:
        target_items = df[df['menu_item'].isin(focus_items)].copy()
    else:
        target_items = df[df['category'] == 'Challenge'].copy()

    if target_items.empty:
        return {
            'scenarios': [],
            'summary': {
                'total_items_analyzed': 0,
                'current_total_profit': 0.0,
                'projected_total_profit': 0.0,
                'profit_increase': 0.0,
                'profit_increase_pct': 0.0
            },
            'top_opportunities': [],
            'summary_text': 'No Challenge items found for profit optimization analysis.'
        }

    # Calculate current totals
    current_total_revenue = target_items['total_revenue'].sum()
    current_total_profit = target_items['total_profit'].sum()
    current_total_quantity = target_items['quantity'].sum()

    # Generate scenarios for each item
    scenarios = []

    for idx, item in target_items.iterrows():
        current_qty = float(item['quantity'])
        current_revenue = float(item['total_revenue'])
        current_profit = float(item['total_profit'])
        item_price = float(item['item_sell_price'])
        item_cost = float(item['item_cost'])
        profit_per_unit = item_price - item_cost

        # Calculate projected metrics
        projected_qty = current_qty * (1 + volume_increase_pct / 100)
        projected_revenue = projected_qty * item_price
        projected_cost = projected_qty * item_cost
        projected_profit = projected_revenue - projected_cost

        # Calculate changes
        revenue_increase = projected_revenue - current_revenue
        profit_increase = projected_profit - current_profit
        profit_increase_pct = (profit_increase / current_profit * 100) if current_profit > 0 else 0

        # Calculate ROI if we invest in marketing (assume 10% of profit increase goes to marketing)
        marketing_investment = profit_increase * 0.10
        net_profit_increase = profit_increase - marketing_investment
        roi = (net_profit_increase / marketing_investment * 100) if marketing_investment > 0 else 0

        scenario = {
            'menu_item': str(item['menu_item']),
            'group': str(item.get('group', 'Unknown')),
            'current_metrics': {
                'quantity': round(current_qty, 2),
                'revenue': round(current_revenue, 2),
                'profit': round(current_profit, 2),
                'profit_margin_pct': round(float(item['profit_margin_pct']), 2)
            },
            'projected_metrics': {
                'quantity': round(projected_qty, 2),
                'revenue': round(projected_revenue, 2),
                'profit': round(projected_profit, 2),
                'profit_margin_pct': round((profit_per_unit / item_price * 100), 2)
            },
            'impact': {
                'quantity_increase': round(projected_qty - current_qty, 2),
                'revenue_increase': round(revenue_increase, 2),
                'profit_increase': round(profit_increase, 2),
                'profit_increase_pct': round(profit_increase_pct, 2),
                'marketing_investment': round(marketing_investment, 2),
                'net_profit_increase': round(net_profit_increase, 2),
                'roi_pct': round(roi, 2)
            }
        }

        scenarios.append(scenario)

    # Sort by profit increase potential
    scenarios_sorted = sorted(scenarios, key=lambda x: x['impact']['profit_increase'], reverse=True)

    # Calculate total projected impact
    total_projected_revenue = sum(s['projected_metrics']['revenue'] for s in scenarios)
    total_projected_profit = sum(s['projected_metrics']['profit'] for s in scenarios)
    total_profit_increase = total_projected_profit - current_total_profit
    total_profit_increase_pct = (total_profit_increase / current_total_profit * 100) if current_total_profit > 0 else 0

    # Get top opportunities
    top_opportunities = scenarios_sorted[:10]

    return {
        'scenario_parameters': {
            'volume_increase_pct': volume_increase_pct,
            'items_analyzed': len(target_items),
            'focus_type': 'challenge_items' if not focus_items else 'custom_items'
        },
        'current_state': {
            'total_quantity': round(current_total_quantity, 2),
            'total_revenue': round(current_total_revenue, 2),
            'total_profit': round(current_total_profit, 2)
        },
        'projected_state': {
            'total_quantity': round(sum(s['projected_metrics']['quantity'] for s in scenarios), 2),
            'total_revenue': round(total_projected_revenue, 2),
            'total_profit': round(total_projected_profit, 2)
        },
        'impact_summary': {
            'quantity_increase': round(sum(s['projected_metrics']['quantity'] for s in scenarios) - current_total_quantity, 2),
            'revenue_increase': round(total_projected_revenue - current_total_revenue, 2),
            'profit_increase': round(total_profit_increase, 2),
            'profit_increase_pct': round(total_profit_increase_pct, 2),
            'total_marketing_investment': round(sum(s['impact']['marketing_investment'] for s in scenarios), 2),
            'net_profit_increase': round(sum(s['impact']['net_profit_increase'] for s in scenarios), 2)
        },
        'scenarios': scenarios_sorted,
        'top_opportunities': [
            {
                'rank': i + 1,
                'menu_item': opp['menu_item'],
                'group': opp['group'],
                'profit_increase': opp['impact']['profit_increase'],
                'roi_pct': opp['impact']['roi_pct'],
                'current_profit': opp['current_metrics']['profit']
            }
            for i, opp in enumerate(top_opportunities)
        ],
        'summary_text': (
            f"Simulating {volume_increase_pct}% volume increase for {len(target_items)} items. "
            f"Current profit: ${current_total_profit:,.2f}. "
            f"Projected profit: ${total_projected_profit:,.2f}. "
            f"Profit increase: ${total_profit_increase:,.2f} ({total_profit_increase_pct:.1f}%). "
            f"Top opportunity: {top_opportunities[0]['menu_item']} with ${top_opportunities[0]['impact']['profit_increase']:,.2f} potential increase."
        ) if top_opportunities else "No opportunities found."
    }


def boston_matrix(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience wrapper around generate_menu_engineering_matrix.

    Returns the matrix analysis using the same 2x2 quadrant approach.
    """
    return generate_menu_engineering_matrix(df)


def challenge_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return Challenge items (high margin, low popularity) — primary marketing targets.
    Sorted by item_profit descending so the biggest margin wins are on top.
    """
    if 'category' not in df.columns:
        return pd.DataFrame()

    challenges = df[df['category'] == 'Challenge'].copy()

    if 'item_profit' in challenges.columns:
        challenges = challenges.sort_values('item_profit', ascending=False)

    return challenges


def star_items(df: pd.DataFrame) -> pd.DataFrame:
    """Return Star items — protect and feature prominently."""
    if 'category' not in df.columns:
        return pd.DataFrame()
    return df[df['category'] == 'Star'].copy()


def dog_items(df: pd.DataFrame) -> pd.DataFrame:
    """Return Dog items — candidates for removal or reinvention."""
    if 'category' not in df.columns:
        return pd.DataFrame()
    return df[df['category'] == 'Dog'].copy()


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Boston Matrix category summary (Star / Challenge / Workhorse / Dog).

    Only works on Menu Engineering DataFrames that have a 'category' column.

    Returns DataFrame indexed by category with item_count, total_revenue, total_profit,
    avg_profit_margin_pct, and pct_of_total_revenue.
    """
    if df.empty or 'category' not in df.columns:
        return pd.DataFrame()

    rev = _revenue_col(df)
    if rev is None:
        return pd.DataFrame()

    agg = {rev: 'sum'}
    if 'total_profit' in df.columns:
        agg['total_profit'] = 'sum'
    if 'profit_margin_pct' in df.columns:
        agg['profit_margin_pct'] = 'mean'

    name = _name_col(df)
    if name:
        agg[name] = 'count'

    result = df.groupby('category').agg(agg).round(2)

    rename = {rev: 'total_revenue'}
    if name:
        rename[name] = 'item_count'
    if 'profit_margin_pct' in agg:
        rename['profit_margin_pct'] = 'avg_profit_margin_pct'
    result.rename(columns=rename, inplace=True)

    result['pct_of_total_revenue'] = (result['total_revenue'] / result['total_revenue'].sum() * 100).round(2)

    # Order: Star → Workhorse → Challenge → Dog
    order = ['Star', 'Workhorse', 'Challenge', 'Dog']
    result = result.reindex([c for c in order if c in result.index])
    return result


def quick_summary(df: pd.DataFrame) -> str:
    """
    Return a short natural-language summary suitable for dropping straight
    into a Cowork conversation.
    """
    if df.empty:
        return "No data to summarize."

    rev = _revenue_col(df)
    qty = _qty_col(df)
    name = _name_col(df)

    parts = []
    parts.append(f"**{len(df)} items** analyzed.")

    if rev:
        total = df[rev].sum()
        parts.append(f"Total revenue: **${total:,.0f}**.")

    if qty:
        total_qty = int(df[qty].sum())
        parts.append(f"Total units sold: **{total_qty:,}**.")

    if 'category' in df.columns:
        cats = df['category'].value_counts().to_dict()
        parts.append(
            f"Boston Matrix: {cats.get('Star', 0)} Stars, "
            f"{cats.get('Workhorse', 0)} Workhorses, "
            f"{cats.get('Challenge', 0)} Challenges, "
            f"{cats.get('Dog', 0)} Dogs."
        )

    if name and rev:
        top = df.nlargest(1, rev).iloc[0]
        parts.append(f"Top item: **{top[name]}** (${top[rev]:,.0f}).")

    return " ".join(parts)


if __name__ == "__main__":
    print("Couqley Menu Engineering Analyzer")
    print("=" * 60)
    print("\nMain functions:")
    print("  - menu_marketing_engine(menu_df, top_n=20): Generate marketing plays")
    print("  - generate_menu_engineering_matrix(df): 2x2 quadrant analysis")
    print("  - calculate_profit_optimization(df, volume_increase_pct=30.0): What-if analysis")
    print("  - boston_matrix(df): Wrapper for matrix analysis")
    print("\nHelper functions:")
    print("  - challenge_items(df): High-margin, low-volume items")
    print("  - star_items(df): High-margin, high-volume items")
    print("  - dog_items(df): Low-margin, low-volume items")
    print("  - category_summary(df): Boston Matrix overview")
    print("  - quick_summary(df): One-liner for chat")
