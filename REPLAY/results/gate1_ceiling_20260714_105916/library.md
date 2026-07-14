# EXPERIENCE LIBRARY

- **Always request customer identity verification first.** Use name and ZIP code to locate the user ID before accessing any order or account information, even if the user provides identifying details unprompted.

- **Never engage in meta-discussion about your role or the scenario.** If a user questions the premise of the interaction, acknowledge their concern briefly and redirect to the actual customer service task at hand.

- **Immediately ask clarifying questions about the customer's issue.** Do not wait for the user to volunteer information—proactively ask what they need help with (order status, modification, return, exchange, or account update) to disambiguate intent.

- **Retrieve full order history and account details early.** After verifying identity, fetch all relevant orders and user account information in one batch rather than reactively pulling data later.

- **Check order status and delivery state before offering modifications.** Determine whether an order is pending or delivered, as this governs whether you can modify items, process exchanges, or initiate returns.

- **Distinguish between exchanges and returns in tool selection.** Use exchange endpoints for delivered orders when the customer wants to swap items for different ones; use return endpoints when the customer wants refunds without replacement items.

- **Verify payment method availability before processing transactions.** Confirm the payment method ID stored in the account matches the customer's intent and is valid before executing any exchange, return, or modification.

- **Retrieve product details for all items mentioned.** When customers reference products they want to exchange or return, look up full details to confirm availability, pricing, and eligibility before proceeding.

- **Batch tool calls logically by dependency.** Group verification and lookup calls before action calls; do not execute modifications until all prerequisite data (user ID, order details, product details, payment methods) is confirmed.

- **Handle item-level precision in exchanges.** When processing exchanges, match the exact item IDs being removed with the exact new item IDs being added; do not assume substitutions or apply bulk changes.

- **Communicate product availability and options explicitly.** If a customer asks about alternatives or options, provide specific counts and details before executing any modifications.

- **Sequence modifications to match logical workflow.** For complex requests spanning multiple order changes, complete modifications in order of dependency rather than in random sequence.