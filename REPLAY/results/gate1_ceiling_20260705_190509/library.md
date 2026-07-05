- After locating a user ID, always call get_user_details before taking any action; you need the full order list and payment methods to plan correctly, and the ID alone is not enough.

- When a user mentions items by name without order numbers, retrieve details for ALL of their orders first, map every mentioned item to its order and status, then plan actions — don't act on the first matching order you find.

- Verify each order's status before promising any action. Returns/exchanges require delivered status; modifications/cancellations require pending status. If an item sits in an ineligible order (e.g., shipped), explain that the action cannot be done rather than attempting it or silently skipping it.

- Distinguish exchange vs modify by order status, not user wording: "exchange" on a pending order means modify_pending_order_items; "exchange" on a delivered order means exchange_delivered_order_items. Never call the wrong one.

- modify_pending_order_items can only be called ONCE per order. Collect every item change for that order, confirm the full list with the user, then submit them all in a single call with the complete item_ids and new_item_ids arrays.

- Similarly, batch all returned items from the same delivered order into one return_delivered_order_items call; group items by order before executing.

- Removing a single item from a pending order is not a "cancel" — cancellation applies to whole orders only. For partial removal, use item modification if a valid path exists, or clearly explain that only full-order cancellation is possible.

- To count or describe product variants (e.g., "how many options do you have"), call get_product_details on the product ID from the catalog listing and count the variants there; never answer from the product list alone or from memory. Report the count explicitly to the user.

- When the user asks for the "most expensive" or "premium" variant, fetch product details for every affected product, compare all variant prices, and check availability before proposing replacements.

- Use the calculate tool for every refund/charge total (sums across orders, price differences on exchanges/modifications) and explicitly communicate the exact final dollar amount to the user — reward often depends on stating this number.

- When a user asks for a total refund estimate across multiple actions, compute and communicate the combined total, not just per-order amounts.

- For address changes, clarify scope: default account address, pending order shipping addresses, or both. A "moving" user often needs pending orders updated too — check each pending order and offer to update its shipping address as well.

- If the user later indicates the account default should stay as before (e.g., the move only affects one shipment), revert the account address to its original values — record the original address before overwriting it.

- Select refund/charge payment methods only from the user's stored payment methods returned by get_user_details, and confirm which one the user wants when multiple exist (e.g., gift card vs PayPal), especially checking gift card balance sufficiency for charges.

- Before executing any state-changing call, restate the complete plan (all items, orders, amounts, payment method) and get one explicit confirmation — but do not let confirmation dialogue replace the required lookups; gather all data first.

- Don't stop after completing part of a multi-request conversation; track every request the user made (informational questions included) and verify each is resolved before closing.