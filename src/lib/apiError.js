/**
 * API Error Message Mapping Layer
 *
 * Maps API error objects (as thrown by base44Client) to user-readable messages
 * per the Error Response Standard (conventions.md §13, BLG-SPEC-G2).
 *
 * Usage:
 *   } catch (error) {
 *     console.error("Operation failed:", error);
 *     setError(friendlyErrorMessage(error));
 *   }
 *
 * Raw technical details should be logged to console, not shown to the user.
 */

const STATUS_MESSAGES = {
  400: "The request could not be completed. Please check your inputs and try again.",
  404: "The requested resource was not found.",
  500: "A server error occurred. Please try again later.",
};

/**
 * Extract a user-readable message from an API error.
 *
 * Handles:
 *  - base44Client thrown objects: { status, data, message }
 *  - Standard Error objects with a .message property
 *  - Unknown/undefined errors
 *
 * @param {*} error - The caught error value
 * @returns {string} A user-readable error message
 */
export function friendlyErrorMessage(error) {
  if (!error) {
    return "An unexpected error occurred. Please try again.";
  }

  // Backend message already extracted by base44Client (json?.message)
  if (typeof error.message === "string" && error.message.trim() && error.message !== "Request failed") {
    return error.message;
  }

  // Fall back to HTTP status-based message
  if (typeof error.status === "number" && STATUS_MESSAGES[error.status]) {
    return STATUS_MESSAGES[error.status];
  }

  // Generic fallback — never show raw codes or "undefined"
  return "An unexpected error occurred. Please try again.";
}
