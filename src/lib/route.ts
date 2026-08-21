/**
 * The guided walk (الجولة).
 *
 * The route is an ORDERING, nothing more. Every stop is an entry that already
 * exists, so the words on the route page are the book's, reached through the
 * same content collection the entry pages use — no second copy of the prose,
 * and nothing written specially for the route.
 *
 * There are no walking times, distances or durations here, and none may be
 * added: nobody has measured them. `design/Route.dc.html` shows "about two
 * hours" and per-stop minutes; that is placeholder content on a mockup, not a
 * source. (CLAUDE.md, "Do not invent practical facts".)
 */
import raw from '../../content/data/route.json';
import { PLAN_GATES, PLAN_TOWERS } from './plan';
import type { Lang } from './i18n';

export type RouteStop = {
  n: number;
  /** The entry this stop is. */
  slug: string;
  /** A second entry that belongs to the same stop (the mosque and its oven). */
  also?: string;
  /** A mark on the traced plan, where the stop is one. */
  plan?: string;
  /** The book records the thing itself as gone; only the place remains. */
  gone?: boolean;
};

export const ROUTE: RouteStop[] = raw.stops;

/** Where the walk begins, named from the traced plan. */
export const START_PLAN: string = raw.start.plan;

/**
 * The name of a plan mark, for the small "on the wall" tag a stop can carry.
 * Names come from the plan's OWN legend (traced into wall-plan.json), which is
 * the only source that names all 21 marks — the book's wall entry names fewer.
 */
export function planName(planId: string, lang: Lang): string | undefined {
  const mark =
    PLAN_GATES.find((g) => g.id === planId) ?? PLAN_TOWERS.find((t) => t.id === planId);
  return mark ? (lang === 'ar' ? mark.ar : mark.en) : undefined;
}
