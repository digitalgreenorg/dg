import { Injectable } from '@angular/core';
import { Headers, Http, URLSearchParams, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { Observable } from 'rxjs/Rx';
import { environment } from '../../environments/environment.training';

@Injectable()
export class GraphsService {

  private graphURL = environment.url + "graph_data";

  constructor(private http: Http) { }

  getData(filters): Observable<any> {
    let params: URLSearchParams = new URLSearchParams();
    for (let key in filters.params) {
      params.set(key.toString(), filters.params[key]);
    }

    let requestOptions: RequestOptions = new RequestOptions();
    requestOptions.search = params;

    return this.http.get(this.graphURL, requestOptions)
      .map(response => response.json())
      .catch(this.handleError);
  }
  private handleError(error: any): any {
    console.error('An error occurred', error);
    return Observable.throw(error.json().error || 'Server error');
  }
}
