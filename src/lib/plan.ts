import plan from '../../content/data/wall-plan.json';

/**
 * Dr Al Salmi's plan of the wall, traced into coordinates by
 * work/trace_wall_plan.py. See that file for how each mark was identified.
 *
 * The numbers are positions in a 1000x1000 drawing, not on the earth. The plan
 * is a drawing in a book, traced at 753px wide: good enough to point at a tower,
 * useless for navigation. It carries no latitude or longitude and must never be
 * presented as a survey.
 */
export type PlanMark = {
  id: string;
  x: number;
  y: number;
  /** Where the mark was actually detected, before being snapped onto the circuit. */
  raw: number[];
  /** How far it moved, in plan units. Kept so the snap stays auditable. */
  snapped_by: number;
  /** The name the plan's own legend gives this mark, and how near that label sat. */
  ar?: string;
  en?: string;
  label_distance?: number;
  side: string;
  bearing: number;
};

export type Landmark = { id: string; x: number; y: number; radius: number };

const doc = plan as unknown as {
  source: string;
  traced_by: string;
  caution: string;
  viewBox: [number, number, number, number];
  wall: [number, number][];
  centroid: [number, number];
  towers: PlanMark[];
  gates: PlanMark[];
  landmarks: Landmark[];
  legend: { source: string; labels_found: number; marks_named: number };
};

export const PLAN = doc;
export const WALL_PATH = `M ${doc.wall.map(([x, y]) => `${x} ${y}`).join(' L ')} Z`;
export const PLAN_TOWERS = doc.towers;
export const PLAN_GATES = doc.gates;
export const PLAN_VIEWBOX = doc.viewBox.join(' ');
export const PLAN_LANDMARKS = doc.landmarks ?? [];
export const PLAN_LEGEND = doc.legend;
