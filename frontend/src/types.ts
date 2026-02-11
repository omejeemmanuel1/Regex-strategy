export interface ExtractedItem {
  product_name?: string;
  quantity?: number;
  unit?: string;
  price?: number;
  unit_price?: number;
}

export interface ParseResponse {
  extracted_items: ExtractedItem[];
}

export interface ErrorResponse {
  detail: string;
}