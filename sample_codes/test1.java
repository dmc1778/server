public class ScannerHasNextExample1 {    
   public static void main(String args[]){           
         //Create Scanner object
      try
      {  
         Scanner scan = new Scanner("Hello World!");  
         //Printing the delimiter used  
         System.out.println("Delimiter:" + scan.delimiter());  
         //Print the Strings  
         if (scan != null){
            while (scan.hasNext()) {  
               System.out.println(scan.next());  
            }  
         }
  
         //Close the scanner  
         scan.close();  
      }
      catch(FileNotFoundException e) {
         handle(e);
      }   
   }
}  