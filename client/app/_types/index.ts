export interface MenuItem {
    id: number;
    name: string;
    price: number;
  }
  
  export interface CartItem extends MenuItem {
    quantity: number;
  }
  