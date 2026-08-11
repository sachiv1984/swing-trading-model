'use strict';

import { useState } from "react";
import { ChevronDown, ChevronUp, FileText } from "lucide-react";
import { Link } from "react-router-dom";

const THESIS_SENTENCE_LIMIT = 3;
const RISK_FACTORS_PER_FIELD = 2;
const RISK_FACTORS_LIMIT = 4;

function splitSentences(text) {
  if (!text) return [];
  return text
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function truncateToSentences(text, max) {
  return splitSentences(text).slice(0, max).join(" ");
}

function buildRiskFactors(exitConditions, confirmationCriteria) {
  const fromExit = splitSentences(exitConditions).slice(0, RISK_FACTORS_PER_FIELD);
  const fromConfirmation = splitSentences(confirmationCriteria).slice(0, RISK_FACTORS_PER_FIELD);
  return [...fromExit, ...fromConfirmation].slice(0, RISK_FACTORS_LIMIT);
}

export default function SetupThesisDigestPanel({ plan }) {
  const [expanded, setExpanded] = useState(true);

  const thesis = plan?.setup_thesis?.trim() || "";
  const exitConditions = plan?.early_exit_conditions?.trim() || "";
  const confirmationCriteria = plan?.confirmation_criteria?.trim() || "";

  if (!thesis && !exitConditions) return null;

  const thesisExcerpt = truncateToSentences(thesis, THESIS_SENTENCE_LIMIT);
  const riskFactors = buildRiskFactors(exitConditions, confirmationCriteria);

  return (
    <div
      data-testid="setup-thesis-digest-panel"
      className="rounded-xl bg-slate-800/40 border border-slate-700/60 p-4 space-y-3"
      aria-label="Setup Thesis Digest"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide flex items-center gap-2">
          <FileText className="w-3.5 h-3.5" />
          Setup Thesis Digest
        </h3>
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="text-slate-600 dark:text-slate-400 hover:text-slate-300 transition-colors"
          aria-label={expanded ? "Collapse details" : "Expand details"}
        >
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {expanded && (
        <DigestBody plan={plan} thesisExcerpt={thesisExcerpt} riskFactors={riskFactors} />
      )}
    </div>
  );
}

function DigestBody({ plan, thesisExcerpt, riskFactors }) {
  return (
    <div className="space-y-3">
      {thesisExcerpt && (
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Setup Thesis</p>
          <p className="text-sm text-slate-200">{thesisExcerpt}</p>
        </div>
      )}

      {riskFactors.length > 0 && (
        <div>
          <p className="text-xs text-slate-600 dark:text-slate-400 mb-1">Key Risk Factors</p>
          <ul className="text-sm text-slate-200 list-disc list-inside space-y-0.5">
            {riskFactors.map((factor) => (
              <li key={factor}>{factor}</li>
            ))}
          </ul>
        </div>
      )}

      {plan?.id && (
        <Link
          to={`/TradePlan?edit=${plan.id}&ticker=${plan.ticker || ""}`}
          className="inline-block text-xs text-cyan-400 hover:text-cyan-300 underline"
        >
          View full plan →
        </Link>
      )}
    </div>
  );
}
