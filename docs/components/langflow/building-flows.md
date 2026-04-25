# Building Flows

Flows are directed graphs of components. Each component performs a unit of work — loading data, calling an LLM, parsing output, etc. — and passes results to the next component.

## The Canvas

- **Drag-and-drop:** Drop components from the sidebar onto the canvas.
- **Ports:** Each component exposes typed input/output ports. Compatible ports share a color.
- **Edges:** Drag from an output port to an input port to create a connection.
- **Multi-select:** Hold `Shift` and drag to select multiple components; use `Ctrl/Cmd+C`, `Ctrl/Cmd+V` to duplicate.

## Running a Flow

- Click the **Play** icon on a component to execute up to that point.
- Click **Run** at the top of the canvas to execute the whole flow.
- Outputs are shown inline on each component and in the **Playground** panel.

## Variables and Secrets

Use the **Global Variables** panel (gear icon in the sidebar) to store reusable values and API keys. Reference them from component fields with the variable picker.

## Version Control

- Every save creates a new revision you can revert to from the flow settings menu.
- Export a flow as JSON from the flow menu to commit it to source control.

See also: [Components](./components.md), [Deploying Flows](./deploying-flows.md).
