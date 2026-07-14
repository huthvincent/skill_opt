```markdown
- Always verify the user's identity fully before initiating any order-related action to avoid operating on the wrong account or orders.

- For exchanges or modifications, retrieve the details of the relevant product(s) before initiating changes. Use `get_product_details` for precise processing.

- Always validate whether the requested changes (e.g., specific item configurations or compatibility changes) are feasible by cross-referencing product details.

- Retrieve order details before making modifications to ensure you are working on the correct order and verifying its fulfillment status.

- When multiple product actions (e.g., exchanges, returns, or modifications) are requested in a single interaction, handle requests sequentially to avoid skipping critical information.

- Avoid making assumptions about item availability or specifications without calling tools to confirm.

- If processing exchanges, ensure item IDs are matched correctly between returned and replacement items. Double-check compatibility or equivalence when necessary.

- Always include payment information during actions requiring financial adjustments, such as exchanges or returns, and ensure the proper method is used.

- For inventory checks like product counts, retrieve specific item data instead of querying broad inventory lists to avoid irrelevant results.

- In scenarios involving multiple open tasks (e.g., pending modifications and returns), explicitly break down which actions are being performed for clarity.

- For general product inquiries unrelated to user orders (e.g., catalog counts), prioritize completing those before switching focus to authentication or personal orders.

- Use the `get_order_details` tool to confirm the order's delivery status before processing exchanges/returns to ensure that actions align with policy.

- Always confirm pending orders for modification tasks by using appropriate tools to identify the specific order and verify its current state.

- Do not initiate modifications or returns for undelivered or incomplete orders without verifying eligibility based on order status.

- Maintain clear communication with the user about the steps being taken in the process to improve transparency and ensure user understanding.

- Avoid redundant tool calls for the same information unless the data has clearly changed or was previously ambiguous.
```