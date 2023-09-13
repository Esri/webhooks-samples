using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace receiver.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class WebhookListenerController : Controller
    {
        private readonly IWebHostEnvironment _hostEnvironment;
        public WebhookListenerController(IWebHostEnvironment hostEnvironment)
        {
            _hostEnvironment = hostEnvironment;
        }
        [HttpPost]
        public void Receiver([FromBody] dynamic payload)
        {
            string directoryPath = Path.Combine(_hostEnvironment.ContentRootPath, "WebhookLogs");
            string filePath = Path.Combine(directoryPath, "webhook.txt");
            if (!Directory.Exists(Path.Combine(_hostEnvironment.ContentRootPath, "WebhookLogs")))
            {
                Directory.CreateDirectory(Path.Combine(_hostEnvironment.ContentRootPath, "WebhookLogs"));
            }
            string webHookMessage = JsonSerializer.Serialize(payload);

            using (StreamWriter sw = System.IO.File.AppendText(filePath))
            {
                sw.WriteLine(webHookMessage);
            }
        }
        [HttpGet]
        public string Reader()
        {
            return System.IO.File.ReadAllText(Path.Combine(_hostEnvironment.ContentRootPath, "WebhookLogs", "webhook.txt"));
        }
    }
}
