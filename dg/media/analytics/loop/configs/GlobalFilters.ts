export const globalFiltersConfig = {
    'filter0': {
        name: 'Country',
        show: true,
        child: true,
        data:[],
        default:'',
        dependencies:false
    },
    'filter1': {
        name: 'Partner',
        show: true,
        child: false,
        data:[],
        default:'',
        dependencies:true
    },
}