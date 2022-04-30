import { ApolloServer } from "apollo-server";
import pkg from "@prisma/client";

const { PrismaClient } = pkg;
const db = new PrismaClient();

// 스키마
const typeDefs = `
    type News {
        id:Int!
        content:String!
        url:String!
    }
    type Query {
        totalNews: Int!
        readNews(id:Int!):News
    }
    type Mutation {
        insertNews(url:String!, contentId:String!, content:String!, uploadTime:String, editTime:String): Boolean!
    }
`;

// 리졸버
const resolvers = {
    Query: {
        totalNews: () => 100,
        readNews: async (_, { id }, ___) => {
            return db.news.findUnique({
                where: {
                    id
                }
            })
        }
    },
    Mutation: {
        insertNews: async (_, { url, contentId, content, uploadTime, editTime }, ___) => {
            let result = true
            try {
                await db.news.create({
                    data: {
                        url,
                        contentId,
                        content,
                        uploadTime,
                        editTime
                    }
                })
            }
            catch {
                result = false
            }
            return result
        }
    }
};

// 서버 인스턴스 생성
const server = new ApolloServer({
    typeDefs,
    resolvers,
});

// 서버 구동
server
    .listen()
    .then(({ url }) => console.log(`GraphQL Service running on ${url}`));