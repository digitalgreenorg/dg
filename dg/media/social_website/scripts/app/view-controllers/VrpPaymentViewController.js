define(function (require) {
    'use strict';
    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var jQuery = require('jquery');
    var jQ = require('libs/external/jquery.blockUI');
    var Select2 = require('libs/external/select2');
    var HighChart = require('libs/external/highcharts');
    var datatables = require('datatables');
    var DistrictDataFeed = require('app/libs/DistrictDataFeed');
    var BlockDataFeed = require('app/libs/BlockDataFeed');
    var VrpPaymentDataFeed = require('app/libs/VrpPaymentDataFeed');
    var tableTools = require('TableTools');
    var monthpicker = require('libs/external/jquery.mtz.monthpicker');
    var districtTemplate = require('text!app/views/district.html');
    var blockTemplate = require('text!app/views/block.html');

    var VrpPaymentViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function ($referenceBase) {
            this.base($referenceBase);
            this.initSelect2();
            return this;
        },

        _initReferences: function ($referenceBase) {
            this.base();
            var references = this._references;
            references.districtdataFeed = new DistrictDataFeed();
            references.blockdataFeed = new BlockDataFeed();
            references.vrppaymentdataFeed = new VrpPaymentDataFeed();
            references.$analyticsWrapper = $referenceBase;
            references.$districtContainer = $referenceBase.find('.js-district-container');
            references.$blockContainer = $referenceBase.find('.js-block-container');
            references.$goButton = $referenceBase.find('.js-go-btn');
            references.$partnerList = $referenceBase.find('.js-partnerlist');
            references.$loadingTable = $referenceBase.find('#loading');
            references.$reportTable = $referenceBase.find('#paymenttable');
            references.$startPeriod = $referenceBase.find('.js-startperiod');
            references.$endPeriod = $referenceBase.find('.js-endperiod');
            references.$starExplanation = $referenceBase.find('.js-explanation');
        },

        _initEvents: function () {
            this.base();
            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDistrictDataProcessed = this._onDistrictDataProcessed.bind(this);
            references.districtdataFeed.on('dataProcessed', boundFunctions.onDistrictDataProcessed);

            boundFunctions.onBlockDataProcessed = this._onBlockDataProcessed.bind(this);
            references.blockdataFeed.on('dataProcessed', boundFunctions.onBlockDataProcessed);

            boundFunctions.onVrpPaymentDataProcessed = this._onVrpPaymentDataProcessed.bind(this);
            references.vrppaymentdataFeed.on('dataProcessed', boundFunctions.onVrpPaymentDataProcessed);

            boundFunctions.onGoBtnClick = this._onGoBtnClick.bind(this);
            references.$goButton.on("click", boundFunctions.onGoBtnClick);

            boundFunctions.onPartnerChosen = this._onPartnerChosen.bind(this);
            references.$partnerList.on('change', this._boundFunctions.onPartnerChosen);

            boundFunctions.onFromInputClick = this._onFromInputClick.bind(this);
            references.$startPeriod.on('mouseover', boundFunctions.onFromInputClick);

            boundFunctions.onToInputClick = this._onToInputClick.bind(this);
            references.$endPeriod.on('mouseover', boundFunctions.onToInputClick);
        },

        getDistrict: function () {
            var districtData = this._references.districtdataFeed.getDistrict();
            if (districtData == false) {
                return false;
            }
            this._renderDistrict(districtData);
            this.initSelect2();
        },

        getBlock: function () {
            var blockData = this._references.blockdataFeed.getBlock();
            if (blockData == false) {
                return false;
            }
            this._renderBlock(blockData);
            this.initSelect2();
        },

        _onFromInputClick: function () {
            this._renderFromInput();
        },

        _onToInputClick: function () {
            this._renderToInput();
        },
        _onDistrictDataProcessed: function () {
            this.getDistrict();
        },

        _onBlockDataProcessed: function () {
            this.getBlock();
        },

        _onVrpPaymentDataProcessed: function () {
            this.makeReport();
        },

        _renderFromInput: function(){
            var references = this._references;
            references.$startPeriod.monthpicker();
        },

        _renderToInput: function(){
            var references = this._references;
            references.$endPeriod.monthpicker();
        },

        _renderDistrict: function (districtData) {
            var references = this._references;
            var renderData = {
                district: districtData
            };
            var renderedDistrict = viewRenderer.render(districtTemplate, renderData);
            this._references.$districtContainer.html(renderedDistrict);

            references.$districtList = jQuery('.js-districtlist');

            this._boundFunctions.onDistrictChosen = this._onDistrictChosen.bind(this);
            references.$districtList.on('change', this._boundFunctions.onDistrictChosen);

        },

        _renderBlock: function (blockData) {
            var references = this._references;
            var renderData = {
                block: blockData
            };
            var renderedBlock = viewRenderer.render(blockTemplate, renderData);
            this._references.$blockContainer.html(renderedBlock);

            references.$blockList = jQuery('.js-blocklist');

        },

        initSelect2: function () {
            var references = this._references;
            try {
                $(".chosen-select").select2({no_results_text: "No results match", width: "100%", placeholder: "Choose Block"});
            }
            catch (err) {
                $("select.chosen-select").select2({no_results_text: "No results match", width: "100%", placeholder: "Choose Block"});
            }

        },

        _onPartnerChosen: function () {
            var references = this._references;

            if (references.$partnerList.val() != "") {
                references.districtdataFeed.addInputParam('limit', false, 0);
                references.districtdataFeed.setInputParam('limit', 0, false);
                references.districtdataFeed.addInputParam('partner', false, references.$partnerList.val());
                references.districtdataFeed.setInputParam('partner', references.$partnerList.val(), false);
                this.getDistrict();
            }
            else {
                //TODO: What happens if value becomes default again
            }
        },

        _onDistrictChosen: function () {
            var references = this._references;
            if (references.$districtList.val() != "") {
                references.blockdataFeed.addInputParam('limit', false, 0);
                references.blockdataFeed.setInputParam('limit', 0, false);
                references.blockdataFeed.addInputParam('partner', false, references.$partnerList.val());
                references.blockdataFeed.setInputParam('partner', references.$partnerList.val(), false);
                references.blockdataFeed.addInputParam('district', false, references.$districtList.val());
                references.blockdataFeed.setInputParam('district', references.$districtList.val(), false);
                this.getBlock();
            }
            else {
                //TODO: What happens if value becomes default again
            }
        },

        _onGoBtnClick: function (e) {
            e.preventDefault();
            var references = this._references;

            if (references.$startPeriod.val() == "" || references.$endPeriod.val() == "" || references.$partnerList.val() == "" || references.$districtList.val() == "" ||  references.$blockList.val() == "" ) {
                alert("Information Incomplete! Please fill missing entries");
            }

            else {
                 $(document).ready(function () {
                    $.blockUI({ css: {
                        border: 'none',
                        padding: '15px',
                        backgroundColor: '#000',
                        '-webkit-border-radius': '10px',
                        '-moz-border-radius': '10px',
                        opacity: .5,
                        color: '#ffffff'
                    } });
                });

                if (references.$blockList.val() != "") {
                    references.vrppaymentdataFeed.addInputParam('limit', false, 0);
                    references.vrppaymentdataFeed.setInputParam('limit', 0, false);
                    references.vrppaymentdataFeed.addInputParam('partner', false, references.$partnerList.val());
                    references.vrppaymentdataFeed.setInputParam('partner', references.$partnerList.val(), false);
                    references.vrppaymentdataFeed.addInputParam('district', false, references.$districtList.val());
                    references.vrppaymentdataFeed.setInputParam('district', references.$districtList.val(), false);
                    references.vrppaymentdataFeed.addInputParam('block', false, references.$blockList.val());
                    references.vrppaymentdataFeed.setInputParam('block', references.$blockList.val(), false);
                    references.vrppaymentdataFeed.addInputParam('startperiod', false, references.$startPeriod.val());
                    references.vrppaymentdataFeed.setInputParam('startperiod', references.$startPeriod.val(), false);
                    references.vrppaymentdataFeed.addInputParam('endperiod', false, references.$endPeriod.val());
                    references.vrppaymentdataFeed.setInputParam('endperiod', references.$endPeriod.val(), false);
                    this.makeReport();
                }
                else {
                    //TODO: What happens if value becomes default again
                }
            }
        },


        makeReport: function () {
            var paymentReportData = this._references.vrppaymentdataFeed.getReport();
            if (paymentReportData == false) {
                return false;
            }
            this._renderReport(paymentReportData);
        },


        _renderReport: function (reportData) {
            var references = this._references;
            $.unblockUI();
            var renderData = {
                report: reportData
            };

            jQuery(references.$starExplanation).removeClass('hidden');
            references.$reportTable.DataTable({
                "sDom": 'T<"clear">lfrtip',
                destroy: true,
                "bAutoWidth": false,
                "aoColumns": [
                    {sTitle: "S.No"},
                    {sTitle: "Name"},
                    {sTitle: "Village"},
                    {sTitle: "Total Screenings"},
                    {sTitle: "Successful Screening *"},
                    {sTitle: "Successful Video Adoptions **"},
                    {sTitle: "Amount"}
                ],
                "aaData": renderData['report'],   //aaData takes array_table_values and push data in the table.
                "oTableTools": {
                    "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf"
                }
            });
        },

        setInputParam: function (key, value, disableCacheClearing) {
            this._references.dataFeed.setInputParam(key, value, disableCacheClearing);
        },

        _onInputParamChanged: function () {
            this.getCollectionDropDown();
        },

        destroy: function () {
            this.base();

            // TODO: clean up
        }
    });

    return VrpPaymentViewController;
});
