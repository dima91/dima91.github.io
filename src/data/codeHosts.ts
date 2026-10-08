/** Code hosts a project link may point to, with the name shown in "View on …". */
export const codeHosts: Record<string, string> = {
  'github.com': 'GitHub',
  'gitlab.com': 'GitLab',
};

export function codeHostName(url: string): string | undefined {
  return codeHosts[new URL(url).hostname];
}
