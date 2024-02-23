// import { books } from "../data/books";
// import { Book } from "../types/book";
import { AppSyncResolverEvent } from "aws-lambda";
import axios from 'axios';

export const handler = async (event: AppSyncResolverEvent<object, any>) => {
    try {
        const response = await axios.post('http://localhost:4000/dev/api/handle_graphql', event);
        console.log(response.data)
        return response.data
    } catch (error: any) {
        console.error('Error in fetchData:', error.message);
        throw new Error('Error fetching data');
    }
}
