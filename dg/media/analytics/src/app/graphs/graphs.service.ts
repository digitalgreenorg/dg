import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, URLSearchParams } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class GraphsService {

  private graphURL = 'http://localhost:8000/training/graph_data';

  constructor(private http: Http) { }

  getData(chartType, chartName): Promise<any> {
    return this.http.get(this.graphURL, { 'params': { 'chartType': chartType, 'chartName': chartName } })
      .toPromise()
      .then(response => response.json())
      .catch(this.handleError);
  }
  private handleError(error: any): any {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
