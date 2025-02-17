export interface MenuItem {
    id: number;
    item_name: string;
    price: number;
  }
  
  export interface CartItem extends MenuItem {
    quantity: number;
  }
  