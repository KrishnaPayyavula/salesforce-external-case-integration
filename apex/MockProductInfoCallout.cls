public with sharing class MockProductInfoCallout {
    // Optional: keep paths/constants tidy
    @TestVisible private static final String NAMED_CRED = 'callout:GetProductInfo';
    @TestVisible private static final String PRODUCT_INFO_PATH = '/api/mock/product-info';

    public class ProductInfoRequest {
        @InvocableVariable(label='Case ID' required=true)
        public String caseId;
        @InvocableVariable(label='Product ID' required=true)
        public String productId;
        @InvocableVariable(label='Case Type' required=true)
        public String caseType;
    }
    
    public class ProductInfoResponse {
        @InvocableVariable(label='Success')
        public Boolean success;
        @InvocableVariable(label='Product Name')
        public String productName;
        @InvocableVariable(label='Description')
        public String description;
        @InvocableVariable(label='Formatted Information')
        public String formattedInfo;
        @InvocableVariable(label='Error Message')
        public String errorMessage;
    }
    
    @InvocableMethod(label='Get Mock Product Information' description='Calls external API to get product information')
    public static List<ProductInfoResponse> getProductInformation(List<ProductInfoRequest> requests) {
        List<ProductInfoResponse> responses = new List<ProductInfoResponse>();
        
        for (ProductInfoRequest request : requests) {
            ProductInfoResponse response = new ProductInfoResponse();
            try {
                Http http = new Http();
                HttpRequest httpRequest = new HttpRequest();

                // Use the Named Credential + relative path
                httpRequest.setEndpoint(NAMED_CRED + PRODUCT_INFO_PATH);
                httpRequest.setMethod('POST');
                httpRequest.setHeader('Content-Type', 'application/json');
                httpRequest.setTimeout(30000);

                // Body
                Map<String, Object> requestBody = new Map<String, Object>{
                    'case_id' => request.caseId,
                    'Product__c' => request.productId,
                    'Type' => request.caseType
                };
                httpRequest.setBody(JSON.serialize(requestBody));

                HttpResponse httpResponse = http.send(httpRequest);

                if (httpResponse.getStatusCode() == 200) {
                    Map<String, Object> responseBody = (Map<String, Object>) JSON.deserializeUntyped(httpResponse.getBody());
                    response.success = true;
                    response.productName = (String) responseBody.get('product_name');
                    response.description = (String) responseBody.get('description');
                    response.formattedInfo = formatProductInfo(responseBody);
                } else {
                    response.success = false;
                    response.errorMessage = 'HTTP Error ' + httpResponse.getStatusCode() + ': ' + httpResponse.getStatus();
                    response.formattedInfo = 'Error: Unable to retrieve product information.';
                }

            } catch (Exception e) {
                response.success = false;
                response.errorMessage = 'Exception: ' + e.getMessage();
                response.formattedInfo = 'Error: ' + e.getMessage();
                System.debug('MockProductInfoCallout Error: ' + e.getMessage());
            }
            responses.add(response);
        }
        return responses;
    }

    private static String formatProductInfo(Map<String, Object> responseBody) {
        String formatted = '';
        String productName = (String) responseBody.get('product_name');
        if (productName != null) formatted += 'Product Name: ' + productName + '\n\n';

        String description = (String) responseBody.get('description');
        if (description != null) formatted += 'Description:\n' + description + '\n\n';

        Object specs = responseBody.get('specifications');
        if (specs != null) {
            formatted += 'Specifications:\n';
            Map<String, Object> specMap = (Map<String, Object>) specs;
            for (String key : specMap.keySet()) formatted += '• ' + key + ': ' + String.valueOf(specMap.get(key)) + '\n';
            formatted += '\n';
        }

        List<Object> troubleshooting = (List<Object>) responseBody.get('troubleshooting_steps');
        if (troubleshooting != null && !troubleshooting.isEmpty()) {
            formatted += 'Troubleshooting Steps:\n';
            for (Object step : troubleshooting) formatted += '• ' + String.valueOf(step) + '\n';
            formatted += '\n';
        }

        List<Object> docs = (List<Object>) responseBody.get('documentation_links');
        if (docs != null && !docs.isEmpty()) {
            formatted += 'Documentation Links:\n';
            for (Object doc : docs) formatted += '• ' + String.valueOf(doc) + '\n';
            formatted += '\n';
        }

        Object warranty = responseBody.get('warranty_info');
        if (warranty != null) {
            formatted += 'Warranty Information:\n';
            Map<String, Object> warrantyMap = (Map<String, Object>) warranty;
            for (String key : warrantyMap.keySet()) formatted += '• ' + key + ': ' + String.valueOf(warrantyMap.get(key)) + '\n';
            formatted += '\n';
        }

        Object support = responseBody.get('support_contact');
        if (support != null) {
            formatted += 'Support Contact:\n';
            Map<String, Object> supportMap = (Map<String, Object>) support;
            for (String key : supportMap.keySet()) formatted += '• ' + key + ': ' + String.valueOf(supportMap.get(key)) + '\n';
            formatted += '\n';
        }

        formatted += '---\nRetrieved on: ' + Datetime.now().format() + '\n';
        return formatted;
    }
}