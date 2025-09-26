import type {
  GetServerSideProps,
  GetServerSidePropsContext,
  GetServerSidePropsResult,
  NextApiResponse,
} from "next";
import {
  clearAuthCookies,
  refreshWithToken,
  setRefreshCookie,
  REMEMBER_COOKIE_NAME,
} from "@/server/oidc";

const AUTH_REQUIRED =
  process.env.NEXT_PUBLIC_AUTH_REQUIRED === "1" ||
  process.env.NEXT_PUBLIC_AUTH_REQUIRED?.toLowerCase() === "true";

export function withAuthGuard<P extends Record<string, any> = Record<string, any>>(
  handler?: GetServerSideProps<P>,
) {
  return async (context: GetServerSidePropsContext): Promise<GetServerSidePropsResult<P>> => {
    if (!AUTH_REQUIRED) {
      if (handler) {
        return handler(context);
      }
      return { props: {} as P };
    }

    const refreshToken = context.req.cookies?.refresh_token;
    const rememberCookie = context.req.cookies?.[REMEMBER_COOKIE_NAME];
    const remember = rememberCookie === "1";
    const returnTo = context.resolvedUrl || "/";

    if (!refreshToken) {
      return {
        redirect: {
          destination: `/login?returnTo=${encodeURIComponent(returnTo)}`,
          permanent: false,
        },
      };
    }

    try {
      const tokenResponse = await refreshWithToken(refreshToken);
      if (tokenResponse.refresh_token) {
        setRefreshCookie(
          (context.res as unknown) as NextApiResponse,
          tokenResponse.refresh_token,
          tokenResponse.refresh_expires_in,
          {
            remember,
          },
        );
      }

      if (handler) {
        return handler(context);
      }
      return { props: {} as P };
    } catch (error: any) {
      clearAuthCookies((context.res as unknown) as NextApiResponse);
      const destination = `/login?returnTo=${encodeURIComponent(returnTo)}`;
      return {
        redirect: {
          destination,
          permanent: false,
        },
      };
    }
  };
}
