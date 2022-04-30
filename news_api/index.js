import { ApolloServer } from "apollo-server";
import pkg from "@prisma/client";

const { PrismaClient } = pkg;
const db = new PrismaClient();

const BUFFER_MAX = 5;

// 스키마
const typeDefs = `
    type News {
        id:Int!
        content:String!
        url:String!
    }
    type Query {
        readNews(id:Int!):News
    }
    type Mutation {
        insertNews(url:String!, contentId:String!, content:String!, uploadTime:String, editTime:String): Boolean!
    }
`;

// 리졸버
const resolvers = {
  Query: {
    readNews: async (_, { id }, ___) => {
      const result = await db.news.findUnique({
        where: {
          id,
        },
      });
      await db.news.delete({
        where: {
          id,
        },
      });
      return result;
    },
  },
  Mutation: {
    insertNews: async (
      _,
      { url, contentId, content, uploadTime, editTime },
      ___
    ) => {
      let result = true;
      try {
        const newsNum = await db.news.count();
        if (newsNum >= BUFFER_MAX) {
          const newsLast = await db.news.findFirst({
            select: { id: true },
            orderBy: { id: "asc" },
          });
          await db.news.delete({
            where: { id: newsLast.id },
          });
        }

        await db.news.create({
          data: {
            url,
            contentId,
            content,
            uploadTime,
            editTime,
          },
        });
      } catch (e) {
        console.log(e);
        result = false;
      }
      return result;
    },
  },
};

// 서버 인스턴스 생성
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

// 서버 구동
server
  .listen({
    port: 1000,
  })
  .then(({ url }) => console.log(`GraphQL Service running on ${url}`));
