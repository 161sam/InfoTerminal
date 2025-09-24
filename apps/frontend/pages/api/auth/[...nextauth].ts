import NextAuth from "next-auth";
import KeycloakProvider from "next-auth/providers/keycloak";

export const authOptions = {
  providers: [
    KeycloakProvider({
      issuer: process.env.KEYCLOAK_ISSUER,
      clientId: process.env.KEYCLOAK_CLIENT_ID!,
      clientSecret: "", // public client
    }),
  ],
  session: { strategy: "jwt" },
};
const handler = NextAuth(authOptions as any);
export { handler as GET, handler as POST };
export default handler;
