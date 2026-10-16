import type { LucideIcon } from "lucide-react";

import { TooltipTrigger } from "./TooltipTrigger";

export type SummaryMetricItem = {
  id: string;
  label: string;
  value: string;
  description: string;
  detail?: string;
  Icon: LucideIcon;
};

type SummaryMetricsProps = {
  items: SummaryMetricItem[];
  className?: string;
};

export function SummaryMetrics({ items, className }: SummaryMetricsProps) {
  return (
    <div className={`summary-metrics${className ? ` ${className}` : ""}`}>
      {items.map(({ id, label, value, description, detail, Icon }) => (
        <TooltipTrigger
          key={id}
          as="span"
          ariaLabel={`${label}: ${value}`}
          className={`summary-metric summary-metric-${id}`}
          content={(
            <span className="summary-metric-tooltip">
              <strong>{label}</strong>
              <span>{description}</span>
              {detail ? <span className="summary-metric-tooltip-detail">{detail}</span> : null}
            </span>
          )}
          pinOnClick={false}
        >
          <Icon className="summary-metric-icon" size={14} aria-hidden="true" />
          <span className="summary-metric-value">{value}</span>
        </TooltipTrigger>
      ))}
    </div>
  );
}
