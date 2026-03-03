import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function Login() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Sign in</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Input placeholder="Email" />
          <Input placeholder="Password" type="password" />
          <Button className="w-full">Login</Button>
          <p className="text-sm text-muted-foreground">
            (Demo UI only — backend later)
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
