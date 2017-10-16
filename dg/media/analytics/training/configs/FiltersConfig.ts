export const filterConfig = {
  'filter0': {
    name: 'Assessment',
    show: false,
    expand: false,
    initialLoad: true
  },
  'filter1': {
    name: 'Country',
    show: false,
    expand: false
  },
  'filter2': {
    name: 'State',
    show: true,
    parent: 'Country',
    expand: false,
    initialLoad: true
  },
  'filter3': {
    name: 'Trainer',
    show: true,
    parent: 'State',
    expand: false
  },
  'filter4': {
    name: 'date',
    show: true
  },
}
