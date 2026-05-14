# Building Flows

Flows are directed graphs of components. Each component performs a unit of work — loading data, calling an LLM, parsing output, etc. — and passes its result to the next component.

## The Canvas

- **Drag-and-drop:** Drop components from the sidebar onto the canvas.
- **Ports:** Each component exposes typed input/output ports. Compatible ports share a colour. Hover over a port to see its type.
- **Edges:** Drag from an output port to a compatible input port to connect components.
- **Multi-select:** Hold `Shift` and drag to select multiple components. Use `Ctrl/Cmd+C` and `Ctrl/Cmd+V` to duplicate a selection.
- **Pan and zoom:** Scroll to zoom, click and drag the canvas background to pan. Use the minimap in the corner for large flows.

## Running a Flow

- Click the **Play** icon on a component to execute the flow up to that point. The output appears inline on the component.
- Click **Run** at the top of the canvas to execute the entire flow.
- Outputs are also shown in the **Playground** panel (chat interface for chat flows).

## Configuring Components

1. Click any component on the canvas to open its **side panel**.
2. Fill in required fields (marked with `*`).
3. Toggle **Advanced** to reveal less-common settings such as timeouts, retries, and model parameters.
4. Use the **Code** tab to view the underlying Python class or write a custom implementation.

Some fields support **Global Variable** references — click the variable picker icon in the field to select a stored secret instead of typing a value directly.

## Variables and Secrets

Use **Settings → Global Variables** (gear icon in the sidebar) to store reusable values and secrets such as API keys. Global variables are:
- Encrypted at rest in the Langflow database.
- Referenced from any component field via the variable picker.
- Baked into the pod Secret when a flow is [deployed](./deploying-flows.md).

> **Important:** When deploying a flow that uses global variables, those variables must be defined in your settings before deployment. Missing variables will cause the deployment creation to fail with an error listing the undefined names.

## Version Control

- Every save creates a new revision. Open the flow menu (pencil icon in the header) and choose **Version history** to view and restore past versions.
- Export a flow as JSON via the flow menu → **Export** to commit it to source control or share it with others.
- Import a JSON flow via **New Flow → Import**.

## Organizing Flows into Projects

Flows live inside **projects** (folders). Create a project from the main flows page. Projects can be shared with other DKubeX users from the project settings menu.

See also: [Components](./components.md), [Deploying Flows](./deploying-flows.md).
