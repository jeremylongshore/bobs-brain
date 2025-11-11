import { GenkitError } from "@genkit-ai/core";
async function checkOperation(registry, operation) {
  if (!operation.action) {
    throw new GenkitError({
      status: "INVALID_ARGUMENT",
      message: "Provided operation is missing original request information"
    });
  }
  const backgroundAction = await registry.lookupBackgroundAction(
    operation.action
  );
  if (!backgroundAction) {
    throw new GenkitError({
      status: "INVALID_ARGUMENT",
      message: `Failed to resolve background action from original request: ${operation.action}`
    });
  }
  return await backgroundAction.check(operation);
}
export {
  checkOperation
};
//# sourceMappingURL=check-operation.mjs.map