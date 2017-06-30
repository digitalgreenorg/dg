import { Component, OnInit, ViewChild, ElementRef, ViewContainerRef } from '@angular/core';
import { DatePipe } from '@angular/common';
import { IMyOptions } from 'mydatepicker';
import { Filter } from './filter';
import { FilterElement } from './filter-element';
import { GetFilterDataService } from '../get-filter-data.service';
import { SharedService } from '../shared.service';
import { environment } from '../../environments/environment.training';

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
  @ViewChild('sideNavContent') sideNavContent : ElementRef;
  filter_list: Filter[] = new Array<Filter>();
  filter: Filter;
  showDateFilter: boolean = false;
  invalidDate: boolean = false;
  invalidDateMessage: string;
  private f_list = {};
  private date = new Date();
  public endModel = {
    date: {
      day: this.date.getDate(),
      month: this.date.getMonth() + 1,
      year: this.date.getFullYear()
    }
  };
  public startModel = {
    date: {
      day: new Date(this.date.setDate(this.date.getDate() + 1)).getDate(),
      month: new Date(this.date.setMonth(this.date.getMonth() + 1)).getMonth(),
      year: new Date(this.date.setFullYear(this.date.getFullYear() - 1)).getFullYear()
    }
  };

  private myDatePickerOptions: IMyOptions = {
    dateFormat: 'dd-mm-yyyy',
    alignSelectorRight: true,
    showClearDateBtn: false,
    // editableDateField: false,
    indicateInvalidDate: true,
    inline: false,
    maxYear: this.date.getFullYear() + 1,
    selectionTxtFontSize: '16px',
  };

  constructor(private myElement: ElementRef, private getFilterData: GetFilterDataService, private _sharedService: SharedService, private datepipe: DatePipe) {
  }

  ngOnInit() {

    this.getFilterData.getData().subscribe(val => {
      for (let data of val) {
        if (data['name'] === 'date' && data['visible'] == true) {
          this.showDateFilter = true;
        }
        else {
          this.filter = new Filter();
          this.filter.heading = data['name'];
          this.filter.expand = false;
          this.filter.element = new Array<FilterElement>();
          for (let val of data['data']) {
            let filterElement = new FilterElement();
            filterElement.id = val['id'];
            filterElement.value = val['value'];
            filterElement.checked = false;

            this.filter.element.push(filterElement);
          }
          this.filter_list.push(this.filter);
        }
      }
    });
  }

  closeNav() {
    this.mySidenav.nativeElement.style.width = '0px';
    this.sideNavContent.nativeElement.style.display = 'none';
  }

  openNav() {
    this.mySidenav.nativeElement.style.width = '320px';
    this.sideNavContent.nativeElement.style.display = 'block';
  }

  applyFilters() {
    this.f_list = {};
    for (let f of this.filter_list) {
      let list = f.element.filter(data => { return data.checked }).map(data => {
        return data.id;
      });
      if (list.length > 0) {
        this.f_list[f.heading] = list;
      }
      this.f_list['apply_filter'] = "true";
    }
    if (this.showDateFilter) {
      this.invalidDate = false;
      try {
        let startDate = this.datepipe.transform(this.startModel.date.year.toString() + '-' + this.startModel.date.month.toString() + '-' + this.startModel.date.day.toString(), 'yyyy-MM-dd');
        let endDate = this.datepipe.transform(this.endModel.date.year.toString() + '-' + this.endModel.date.month.toString() + '-' + this.endModel.date.day.toString(), 'yyyy-MM-dd');
        let s_date = new Date(startDate);
        let e_date = new Date(endDate);
        if (s_date < e_date) {
          this.f_list['start_date'] = startDate;
          this.f_list['end_date'] = endDate;
        } else {
          this.invalidDate = true;
          this.invalidDateMessage = "* End date cannot be smaller than start date."
        }
      } catch (err) {
        this.invalidDate = true;
        this.invalidDateMessage = "* Invalid date entered."
      }
    }
    if (!this.invalidDate) {
      this.getDatatest();
      this.closeNav();
    }
  }

  getDatatest(): any {
    let argstest = {
      webUrl: environment.url + "getData",
      params: this.f_list
    }
    this._sharedService.publishData(argstest);
  }

  handleClick(event) {
    let clickedComponent = event.target;
    let inside = false;
    do {
      if (clickedComponent === this.myElement.nativeElement) {
        inside = true;
      }
      clickedComponent = clickedComponent.parentNode;
    } while (clickedComponent);

    if (inside) {
    } else {
      this.closeNav();
    }
  }
}
