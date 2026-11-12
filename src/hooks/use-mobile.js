import * as React from "react"

const MOBILE_BREAKPOINT = 768

export function useIsMobile() {
  // Read the width on the first render, so a phone never renders the
  // desktop layout first and then swaps (ST-02, BLG-FE-261, v9.17).
  const [isMobile, setIsMobile] = React.useState(() =>
    typeof window === "undefined" ? undefined : window.innerWidth < MOBILE_BREAKPOINT
  )

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }
    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    return () => mql.removeEventListener("change", onChange);
  }, [])

  return !!isMobile
}
