import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FILTER_DATA } from './filter-data';
import { Filter } from './filter';
import { FilterElement } from './filter-element';

@Component({
  selector: 'app-filters',
  host: {
    '(document:click)': 'handleClick($event)',
  },
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.css']
})
export class FiltersComponent implements OnInit {

  @ViewChild('mySidenav') mySidenav: ElementRef;
  public elementref: ElementRef;
  filter_list: Filter[] = new Array<Filter>();
  filter: Filter;
  private showDateFilter: boolean;
  constructor(myElement: ElementRef) {
    this.elementref = myElement;
  }

  ngOnInit() {
    for (let data of FILTER_DATA) {

      if (data['name'] === 'date' && data['visible'] == true) {
        this.showDateFilter = true;
      }
      else {
        this.filter = new Filter();
        this.filter.heading = data['name'];
        this.filter.element = new Array<FilterElement>();
        for (let val of data['data']) {
          let filterElement = new FilterElement();
          filterElement.id = val['id'];
          filterElement.value = val['value'];
          filterElement.checked = true;

          this.filter.element.push(filterElement);
        }
        this.filter_list.push(this.filter);
      }
    }
  }

  closeNav() {
    this.mySidenav.nativeElement.style.width = '0px';
  }

  openNav() {
    this.mySidenav.nativeElement.style.width = '240px';
  }

  applyFilters() {
    console.log(this.filter_list);
  }

  handleClick(event) {
    var clickedComponent = event.target;
    var inside = false;
    do {
      if (clickedComponent === this.elementref.nativeElement) {
        inside = true;
      }
      clickedComponent = clickedComponent.parentNode;
    } while (clickedComponent);

    if (inside) {
      // this.closeNav();
      console.log('inside');
    } else {
      console.log('outside');
      this.closeNav();
    }
  }

}
