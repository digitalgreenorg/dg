import { FilterElement } from './filter-element';

export class Filter {
  heading: string;
  searchTerm: string;
  visible: boolean;
  element: FilterElement[];
  expand : boolean;
}
